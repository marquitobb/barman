import logging
import requests
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class RaspberryPiClient:
    """Client for communicating with the Raspberry Pi API"""

    def __init__(self):
        # If no URL is provided, use the one from environment variables
        self.api_url = os.getenv("raspberry_api_url", "http://localhost:8080")
        # Definir timeout como constante de clase
        self.timeout = 45
        logger.info(f"Raspberry Pi API URL configured: {self.api_url}")

    def prepare_drink(self, ingredients):
        """
        Sends the ingredients to the Raspberry Pi to prepare a drink

        Args:
            ingredients: List of ingredients with their percentages and devices

        Returns:
            dict: API response with success and message
        """
        try:
            payload = {"ingredients": ingredients}
            logger.info(f"Sending request to Raspberry Pi: {payload}")

            response = requests.post(
                f"{self.api_url}/drink",
                json=payload,
                timeout=self.timeout
            )

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            logger.error(f"Communication error with Raspberry Pi: {e}")
            return {
                "success": False,
                "message": f"Communication error: {str(e)}"
            }

    def activate_motor(self, device, duration):
        """
        Activates a specific motor for a determined duration

        Args:
            device: Device identifier (relay_one, relay_two, etc.)
            duration: Duration in seconds

        Returns:
            dict: API response with success and message
        """
        try:
            payload = {"device": device, "duration": duration}
            logger.info(f"Activating motor {device} for {duration} seconds")

            response = requests.post(
                f"{self.api_url}/motors/activate",
                json=payload,
                timeout=self.timeout
            )

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            logger.error(f"Error activating motor {device}: {e}")
            return {
                "success": False, 
                "message": f"Error activating motor: {str(e)}"
            }

