import logging
from telegram import Update
from agents.ollama_agent import OllamaAgent

logger = logging.getLogger(__name__)

class TelegramService:
    """Servicios para la integración con Telegram"""

    def __init__(self):
        # Inicializar el agente de Ollama directamente
        self.ollama_agent = OllamaAgent()

    def process_drink_request(self, update: Update, text: str):
        """Procesar directamente la solicitud de bebida usando el agente Ollama."""
        try:
            # Llamar directamente al agente para generar instrucciones de bebida
            drink_data = self.ollama_agent.generate_drink_instructions(text)
            print("drink_data------------------->")
            print(drink_data)


            # Formatear la respuesta para Telegram
            message = f"🍹 *{drink_data['name']}*\n\n"
            message += f"{drink_data['description']}\n\n"
            message += "*Ingredientes:*\n"

            for ingredient in drink_data['ingredients']:
                message += f"• {ingredient['name']}: {ingredient['percentage']}%\n"

            # Enviar la información de la bebida
            update.message.reply_text(
                message,
                parse_mode='Markdown'
            )

            # Informar que se está preparando la bebida
            update.message.reply_text("¡Tu bebida se está preparando! 🍹")

        except Exception as e:
            logger.error(f"Error al procesar la solicitud con Ollama: {e}")
            update.message.reply_text(
                "Lo siento, ocurrió un error al procesar tu solicitud. Por favor, intenta de nuevo."
            )