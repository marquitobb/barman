import os
import logging
import tempfile
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from .service import TelegramService

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        # Cargar el token desde las variables de entorno
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError("No se encontró el token de Telegram en las variables de entorno")
        
        self.service = TelegramService()
        self.updater = Updater(token=self.token)
        self.dispatcher = self.updater.dispatcher
        
        # Registrar manejadores
        self.register_handlers()
        
        logger.info("Bot de Telegram inicializado")
    
    def register_handlers(self):
        """Registrar todos los manejadores de comandos y mensajes"""
        # Comandos básicos
        self.dispatcher.add_handler(CommandHandler("start", self.start_command))
        self.dispatcher.add_handler(CommandHandler("help", self.help_command))
        self.dispatcher.add_handler(CommandHandler("menu", self.menu_command))
        
        # Manejador de mensajes de voz
        self.dispatcher.add_handler(MessageHandler(Filters.voice, self.handle_voice))
        
        # Manejador de mensajes de texto
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
            
            # Enviar el archivo al server-ai para procesamiento
            self.service.process_audio_file(update, temp_path)
            
            # Eliminar el archivo temporal
            os.unlink(temp_path)
            
        except Exception as e:
            logger.error(f"Error procesando mensaje de voz: {e}")
            update.message.reply_text("Ocurrió un error procesando tu mensaje de voz. Por favor, intenta de nuevo o envía un mensaje de texto.")
    
    def handle_text(self, update: Update, context: CallbackContext):
        """Procesar mensajes de texto."""
        text = update.message.text
        self.service.process_drink_request(update, text)
    
    def error_handler(self, update: Update, context: CallbackContext):
        """Manejar errores."""
        logger.error(f"Error: {context.error} - Update: {update}")
        if update and update.message:
            update.message.reply_text("Lo siento, ocurrió un error. Por favor, intenta de nuevo.")
    
    def start(self):
        """Iniciar el bot."""
        self.updater.start_polling()
        logger.info("Bot iniciado")
    
    def stop(self):
        """Detener el bot."""
        self.updater.stop()
        logger.info("Bot detenido")

