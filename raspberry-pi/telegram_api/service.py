# local imports
import logging
import requests
import os
import json
from controllers.motor_controller import MotorController

# third party imports
from dotenv import load_dotenv
from telegram import Update

# logging configuration
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class TelegramService:

    def __init__(self):
        # URL del servidor de IA
        self.server_ai_url = os.getenv("SERVER_AI_URL", "http://localhost:8000")

        # En lugar de un cliente para llamar a la misma Raspberry Pi,
        # usar directamente el controlador de motores
        self.motor_controller = MotorController()

        logger.info(f"TelegramService inicializado. URL del servidor AI: {self.server_ai_url}")

    def process_drink_request(self, update: Update, text: str):
        """Process the drink request using the server-ai API."""
        try:
            # Call the server-ai API instead of Ollama directly
            logger.info(f"Enviando solicitud a la API: {text}")

            # Realizamos la solicitud a la API del servidor AI
            response = requests.post(
                f"{self.server_ai_url}/barman/drink",
                json={"text": text},
                timeout=30
            )

            # Verificamos si la solicitud fue exitosa
            if response.status_code != 200:
                logger.error(f"Error en la API: {response.status_code} - {response.text}")
                update.message.reply_text(
                    f"Lo siento, el servidor de IA no pudo procesar tu solicitud (Error {response.status_code})."
                )
                return

            # Obtenemos los datos de la bebida de la respuesta
            api_response = response.json()

            if not api_response.get("success", False):
                logger.warning(f"La API devolvió un error: {api_response.get('message')}")
                update.message.reply_text(
                    f"Error: {api_response.get('message', 'Error desconocido al procesar la bebida')}"
                )
                return

            # Extraemos los datos de la bebida
            drink_data = {
                "name": api_response.get("name"),
                "description": api_response.get("description"),
                "ingredients": api_response.get("ingredients", [])
            }

            logger.debug(f"Datos de bebida recibidos: {drink_data}")

            # Format the response for Telegram
            message = f"🍹 *{drink_data['name']}*\n\n"
            message += f"{drink_data['description']}\n\n"
            message += "*Ingredientes:*\n"

            for ingredient in drink_data['ingredients']:
                message += f"• {ingredient['name']}: {ingredient['percentage']}%\n"

            # Send the drink information
            update.message.reply_text(
                message,
                parse_mode='Markdown'
            )

            # Inform that the drink is being prepared
            update.message.reply_text("¡Tu bebida se está preparando! 🍹")

            # Preparar la bebida directamente usando el motor_controller
            success = self.motor_controller.process_drink_request({
                "ingredients": drink_data['ingredients']
            })

            if success:
                logger.info("Bebida preparada correctamente")
                update.message.reply_text("✅ La bebida ha sido preparada correctamente.")
            else:
                logger.warning("Error preparando bebida")
                update.message.reply_text("❌ Error preparando la bebida.")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error de conexión con el servidor de IA: {e}")
            update.message.reply_text(
                "Lo siento, no pude conectar con el servidor de IA. Por favor, inténtalo de nuevo más tarde."
            )
        except Exception as e:
            logger.error(f"Error procesando la solicitud: {e}")
            update.message.reply_text(
                "Lo siento, ha ocurrido un error al procesar tu solicitud. Por favor, inténtalo de nuevo."
            )

