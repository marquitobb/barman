import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from .handlers import MessageHandlers

logger = logging.getLogger(__name__)

class TelegramBot:

    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError("No se encontró el token de Telegram en las variables de entorno")

        self.updater = Updater(token=self.token)
        self.dispatcher = self.updater.dispatcher

        # Inicializar los manejadores sin pasar api_url
        self.handlers = MessageHandlers()
        self._register_handlers()

        logger.info("Bot de Telegram inicializado")

    def _register_handlers(self):
        """Registrar todos los manejadores de comandos y mensajes"""
        # Comandos básicos
        self.dispatcher.add_handler(CommandHandler("start", self.handlers.start_command))
        self.dispatcher.add_handler(CommandHandler("help", self.handlers.help_command))
        self.dispatcher.add_handler(CommandHandler("menu", self.handlers.menu_command))

        # Manejador de mensajes de voz
        self.dispatcher.add_handler(MessageHandler(Filters.voice, self.handlers.handle_voice))

        # Manejador de mensajes de texto
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handlers.handle_text))

        # Manejador de errores
        self.dispatcher.add_error_handler(self.handlers.error_handler)

    def start(self):
        """Iniciar el bot."""
        self.updater.start_polling()
        logger.info("Bot iniciado")

    def stop(self):
        """Detener el bot."""
        self.updater.stop()
        logger.info("Bot detenido")

