import os
import logging
import tempfile
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
from dotenv import load_dotenv
import whisper

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Modelo de Whisper para transcripción
model = None

class TelegramBot:
    def __init__(self, api_url="http://localhost:8000"):
        # self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError("No se encontró el token de Telegram en las variables de entorno")

        self.api_url = api_url
        self.updater = Updater(token=self.token)
        self.dispatcher = self.updater.dispatcher

        # Registrar manejadores
        self.register_handlers()

        # Cargar modelo de Whisper
        global model
        model = whisper.load_model("base")

        logger.info("Bot de Telegram inicializado")

    def register_handlers(self):
        """Registrar todos los manejadores de comandos y mensajes"""
        # Comandos básicos
        self.dispatcher.add_handler(CommandHandler("start", self.start_command))
        self.dispatcher.add_handler(CommandHandler("help", self.help_command))
        self.dispatcher.add_handler(CommandHandler("menu", self.menu_command))
        
        # Manejador de mensajes de voz
        self.dispatcher.add_handler(MessageHandler(Filters.voice, self.handle_voice))
        
        # Manejador de mensajes de texto (para pedir bebidas directamente por texto)
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_text))
        
        # Manejador de errores
        self.dispatcher.add_error_handler(self.error_handler)
    
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
        # Informar al usuario que estamos procesando
        update.message.reply_text("Procesando tu mensaje de voz...")

        try:
            # Descargar el archivo de voz
            voice_file = context.bot.get_file(update.message.voice.file_id)

            # Guardar en un archivo temporal
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_file:
                voice_file.download(custom_path=temp_file.name)
                temp_path = temp_file.name

            # Transcribir el audio con Whisper
            transcription = self.transcribe_audio(temp_path)

            # Eliminar el archivo temporal
            os.unlink(temp_path)

            if not transcription:
                update.message.reply_text("Lo siento, no pude entender el audio. ¿Podrías intentarlo de nuevo?")
                return

            # Mostrar la transcripción
            update.message.reply_text(f"Entendí: '{transcription}'")

            # Procesar la solicitud de bebida
            self.process_drink_request(update, transcription)

        except Exception as e:
            logger.error(f"Error procesando mensaje de voz: {e}")
            update.message.reply_text("Ocurrió un error procesando tu mensaje. Por favor, intenta de nuevo.")
    
    def handle_text(self, update: Update, context: CallbackContext):
        """Procesar mensajes de texto."""
        text = update.message.text
        self.process_drink_request(update, text)
    
    def transcribe_audio(self, audio_path):
        """Transcribir el audio usando Whisper."""
        try:
            global model
            result = model.transcribe(audio_path)
            return result["text"].strip()
        except Exception as e:
            logger.error(f"Error en la transcripción: {e}")
            return None
    
    def process_drink_request(self, update: Update, text):
        """Enviar la solicitud de bebida a la API y manejar la respuesta."""
        try:
            # Enviar la solicitud a la API
            # response = requests.post(
            #     f"{self.api_url}/barman/drink",
            #     json={"text": text}
            # )
            response = 200

            if response == 200:
                drink_data = {
                    "name": "Margarita",
                    "description": "Una refrescante bebida de tequila con limón.",
                    "ingredients": [
                        {"name": "Tequila", "percentage": 50},
                        {"name": "Limón", "percentage": 30},
                        {"name": "Triple Sec", "percentage": 20}
                    ]
                }

                # Formatear la respuesta
                message = f"🍹 *{drink_data['name']}*\n\n"
                message += f"{drink_data['description']}\n\n"
                message += "*Ingredientes:*\n"

                for ingredient in drink_data['ingredients']:
                    message += f"• {ingredient['name']}: {ingredient['percentage']}%\n"

                update.message.reply_text(
                    message, 
                    parse_mode='Markdown'
                )

                # Informar que se está preparando la bebida
                update.message.reply_text("¡Tu bebida se está preparando! 🍹")
            else:
                update.message.reply_text(
                    f"Lo siento, hubo un problema procesando tu solicitud: {response.text}"
                )

        except Exception as e:
            logger.error(f"Error al procesar la solicitud: {e}")
            update.message.reply_text(
                "Lo siento, ocurrió un error al procesar tu solicitud. Por favor, intenta de nuevo."
            )

    def error_handler(self, update: Update, context: CallbackContext):
        """Manejar errores."""
        logger.error(f"Error: {context.error} - Update: {update}")
        if update:
            update.message.reply_text("Lo siento, ocurrió un error. Por favor, intenta de nuevo.")

    def start(self):
        """Iniciar el bot."""
        self.updater.start_polling()
        logger.info("Bot iniciado")

    def stop(self):
        """Detener el bot."""
        self.updater.stop()
        logger.info("Bot detenido")

# Para probar el bot de forma independiente
if __name__ == "__main__":
    bot = TelegramBot()
    bot.start()
    bot.updater.idle()

