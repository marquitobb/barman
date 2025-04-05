import logging
import os
import tempfile
from telegram import Update
from telegram.ext import CallbackContext
from .service import TelegramService
import whisper

logger = logging.getLogger(__name__)

# Modelo global de Whisper para transcripción
model = None

class MessageHandlers:
    """Manejadores para los diferentes tipos de mensajes y comandos"""

    def __init__(self):
        self.service = TelegramService()

        # Inicializar el modelo de Whisper
        global model
        try:
            model = whisper.load_model("base")
            logger.info("Modelo Whisper cargado correctamente")
        except Exception as e:
            logger.error(f"Error al cargar el modelo Whisper: {e}")
            model = None

    def start_command(self, update: Update, context: CallbackContext):
        """Enviar mensaje cuando se recibe el comando /start."""
        user = update.effective_user
        update.message.reply_text(
            f'¡Hola {user.first_name}! Soy el Barman Bot. Puedes pedirme bebidas enviando un mensaje de voz '
            f'o escribiendo directamente lo que quieres. Usa /menu para ver algunas opciones disponibles.'
        )

    def help_command(self, update: Update, context: CallbackContext):
        """Enviar mensaje cuando se recibe el comando /help."""
        update.message.reply_text(
            'Puedo preparar bebidas para ti. Solo dime qué te gustaría beber.\n\n'
            'Comandos disponibles:\n'
            '/start - Iniciar el bot\n'
            '/help - Ver este mensaje de ayuda\n'
            '/menu - Ver algunas bebidas que puedo preparar'
        )

    def menu_command(self, update: Update, context: CallbackContext):
        """Mostrar un menú de bebidas disponibles."""
        update.message.reply_text(
            'Algunas bebidas que puedo preparar:\n\n'
            '🍹 Margarita\n'
            '🥃 Shot de Tequila\n'
            '🍸 Paloma\n'
            '🧛 Vampiro\n\n'
            'También puedes pedirme otras bebidas y veré si puedo prepararlas.'
        )

    def handle_voice(self, update: Update, context: CallbackContext):
        """Procesar mensajes de voz."""
        update.message.reply_text("Procesando tu mensaje de voz...")

        try:
            if model is None:
                update.message.reply_text("Lo siento, la transcripción de voz no está disponible ahora. Por favor, escribe tu pedido.")
                return

            # Descargar el archivo de voz
            voice_file = context.bot.get_file(update.message.voice.file_id)

            # Guardar en un archivo temporal
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_file:
                voice_file.download(custom_path=temp_file.name)
                temp_path = temp_file.name

            # Transcribir el audio con Whisper
            transcription = self._transcribe_audio(temp_path)

            # Eliminar el archivo temporal
            os.unlink(temp_path)

            if not transcription:
                update.message.reply_text("Lo siento, no pude entender el audio. ¿Podrías intentarlo de nuevo?")
                return

            # Mostrar la transcripción
            update.message.reply_text(f"Entendí: '{transcription}'")

            # Procesar la solicitud de bebida
            self.service.process_drink_request(update, transcription)

        except Exception as e:
            logger.error(f"Error procesando mensaje de voz: {e}")
            update.message.reply_text("Ocurrió un error procesando tu mensaje. Por favor, intenta de nuevo.")

    def handle_text(self, update: Update, context: CallbackContext):
        """Procesar mensajes de texto."""
        text = update.message.text
        self.service.process_drink_request(update, text)

    def _transcribe_audio(self, audio_path):
        """Transcribir el audio usando Whisper."""
        try:
            global model
            result = model.transcribe(audio_path)
            return result["text"].strip()
        except Exception as e:
            logger.error(f"Error en la transcripción: {e}")
            return None

    def error_handler(self, update: Update, context: CallbackContext):
        """Manejar errores."""
        logger.error(f"Error: {context.error} - Update: {update}")
        if update:
            update.message.reply_text("Lo siento, ocurrió un error. Por favor, intenta de nuevo.")