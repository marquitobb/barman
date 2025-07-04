from controllers.relay_controller import RelayController

class MotorController:

    def __init__(self):
        # Initialize the relay controller
        self.relay_controller = RelayController()
        # Define the flow rate for each device in ml/second
        self.flow_rates = {
            "relay_one": 20.0,   # 20 ml per second for relay one (tequila)
            "relay_two": 40.0    # 40 ml per second for relay two (soda)
        }
        # Define GPIO pins for each relay
        self.relay_pins = {
            "relay_one": 20,  # GPIO20
            "relay_two": 17   # GPIO17
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

        # Get the GPIO pin for the device
        pin = self.relay_pins.get(device)

        if not pin:
            print(f"Device {device} not recognized")
            return

        if device == "relay_one":
            self.relay_controller.operate_relay_one(pin=pin, duration=seconds)
        elif device == "relay_two":
            self.relay_controller.operate_relay_two(pin=pin, duration=seconds)
        # Add more relays as needed
        else:
            print(f"Device {device} not recognized")

    def process_drink_request(self, drink_request) -> bool:
        try:
            print(f"Drink request: {drink_request}")
            ingredients = drink_request.get("ingredients")
            for ingredient in ingredients:
                self.create_drink(ingredient)
            return True
        except Exception as e:
            print(f"Error processing drink request: {e}")
            return False

    def create_drink(self, drink_data):
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
    # TODO: hice to have with camera validate the size of the glass
    def evaluate_size_glasse(self) -> int:
        # TODO: call api to evaluate the size of the glass
        # get_glass_size = self.api_client.get_glass_size()

        # TODO: return the size of the glass in milliliters
        return 200

