import requests
import json
from typing import Dict, Any, Optional
from .models import DrinkRequest, DrinkResponse

class ApiClient:
    """Client to interact with the AI server API"""

    def __init__(
        self,
        base_url: str = "http://localhost:8000"
    ):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }


    def process_drink_request(
        self,
        text: str
    ) -> Optional[Dict[str, Any]]:
        """
        Sends a drink request text to be processed

        Args:
            text: Text of the drink request

        Returns:
            Dictionary with the response or None if there is an error
        """
        endpoint = f"{self.base_url}/barman/drink"
        try:
            print(f"Text: {text}")
            drink_request = DrinkRequest(text=text)
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=drink_request.dict()
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making the request: {e}")
            return None


    def get_glass_size(
        self
    ) -> Optional[int]:
        """
        Gets the size of the glass from the API

        Returns:
            Size of the glass in millilit
        """
        endpoint = f"{self.base_url}/barman/glass"
        try:
            response
            response = requests.get
            response.raise_for_status()
            return response.json().get("size")
        except requests.exceptions.RequestException as e:
            print(f"Error making the request: {e}")
            return None

