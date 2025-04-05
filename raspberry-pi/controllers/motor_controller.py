from controllers.relay_controller import RelayController
import time
import requests

class MotorController:

    def __init__(self):
        # Initialize the relay controller
        self.relay_controller = RelayController(
            relay_pin_one=17,  # GPIO17
            relay_pin_two=27   # GPIO27
        )
        # Define the flow rate for each device in ml/second
        self.flow_rates = {
            "relay_one": 20.0,   # 20 ml per second for relay one (tequila)
            "relay_two": 30.0    # 30 ml per second for relay two (soda)
        }

    def ml_to_seconds(self, ml: float, device: str) -> float:
        """
        Converts milliliters to seconds based on the device's flow rate

        Args:
            ml: Amount in milliliters to dispense
            device: Device to use (relay_one, relay_two, etc.)

        Returns:
            Time in seconds that the motor should be on
        """
        # Get the flow rate of the device or use a default value
        flow_rate = self.flow_rates.get(device, 20.0)  # ml/second

        # Calculate the time in seconds
        seconds = ml / flow_rate

        # Ensure minimum time is 0.5 seconds
        return max(seconds, 0.5)

    def activate_motor(self, device: str, seconds: float):
        """
        Activates the corresponding motor for the specified time

        Args:
            device: Device to activate (relay_one, relay_two, etc.)
            seconds: Time in seconds that the motor should be on
        """
        print(f"Activating {device} for {seconds:.2f} seconds")

        if device == "relay_one":
            self.relay_controller.turn_on_relay_one(duration=seconds)
        elif device == "relay_two":
            self.relay_controller.turn_on_relay_two(duration=seconds)
        # Add more relays as needed
        else:
            print(f"Device {device} not recognized")
        self.relay_controller.cleanup()

    def process_drink_request(
        self,
        text: str
    ) -> bool:
        try:
            print(f"Text: {text}")
            ingredients = text.get("ingredients")
            for ingredient in ingredients:
                # Si el dispositivo es relay_three, cambiarlo a relay_two
                if ingredient.get('device') == 'relay_three':
                    ingredient['device'] = 'relay_two'
                self.create_drink(ingredient)
            return True
        except Exception as e:
            print(f"Error processing drink request: {e}")
            return False

    def create_drink(
        self,
        drink_data
    ):
        print(f"Drink data: {drink_data}")
        # Get the total glass size in milliliters
        total_size_ml: int = self.evaluate_size_glasse()
        print(f"Total glass size: {total_size_ml} ml")

        # Get the ingredient percentage
        print(f"Ingredient percentage: {drink_data.get('percentage')}%")
        porcentage: int = int(drink_data.get('percentage'))

        # Calculate the exact amount in milliliters
        amount_ml: float = (total_size_ml * porcentage) / 100
        print(f"Dispensing {amount_ml} ml of {drink_data.get('name')}")

        # Get the device from drink_data
        device = drink_data.get('device')
        # Si el dispositivo es relay_three, cambiarlo a relay_two
        if device == 'relay_three':
            device = 'relay_two'

        # convert milliliters to seconds
        seconds = self.ml_to_seconds(amount_ml, device)

        # Activate the motor
        self.activate_motor(device, seconds)

        print(f"Ingredient: {drink_data.get('name')} dispensed")

    # TODO: Implement the method to evaluate the size of the glass
    def evaluate_size_glasse(
        self
    ) -> int:
        # TODO: call api to evaluate the size of the glass
        # get_glass_size = self.api_client.get_glass_size()

        # TODO: return the size of the glass in milliliters
        return 500

