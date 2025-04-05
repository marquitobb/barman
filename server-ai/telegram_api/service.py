import logging
import requests
import os
from dotenv import load_dotenv
from telegram import Update
from agents.ollama_agent import OllamaAgent
from motors.relay_api import RaspberryPiClient

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class TelegramService:

    def __init__(self):
        # Initialize the Ollama agent directly
        self.ollama_agent = OllamaAgent()

        # Initialize the Raspberry Pi client
        self.raspberry_client = RaspberryPiClient()


    def process_drink_request(self, update: Update, text: str):
        """Process the drink request directly using the Ollama agent."""
        try:
            # Call the agent directly to generate drink instructions
            drink_data = self.ollama_agent.generate_drink_instructions(text)
            logger.debug("drink data------------------->")
            logger.debug(f"Generated drink data: {drink_data}")

            # Format the response for Telegram
            message = f"🍹 *{drink_data['name']}*\n\n"
            message += f"{drink_data['description']}\n\n"
            message += "*Ingredients:*\n"

            for ingredient in drink_data['ingredients']:
                message += f"• {ingredient['name']}: {ingredient['percentage']}%\n"

            # Send the drink information
            update.message.reply_text(
                message,
                parse_mode='Markdown'
            )

            # Inform that the drink is being prepared
            update.message.reply_text("Your drink is being prepared! 🍹")

            # call the Raspberry Pi API to prepare the drink
            result = self.raspberry_client.prepare_drink(drink_data['ingredients'])
            logger.debug("result------------------->")
            logger.debug(f"Result from Raspberry Pi: {result}")

            if result.get("success"):
                logger.info("Bebida preparada correctamente")
                update.message.reply_text("✅ La bebida ha sido preparada correctamente.")
            else:
                logger.warning(f"Error preparando bebida: {result.get('message', 'Error desconocido')}")
                update.message.reply_text(f"❌ Error preparando la bebida: {result.get('message', 'Error desconocido')}")

        except Exception as e:
            logger.error(f"Error processing request with Ollama: {e}")
            update.message.reply_text(
                "Lo siento, ha ocurrido un error al procesar tu solicitud. Por favor, inténtalo de nuevo."
            )

