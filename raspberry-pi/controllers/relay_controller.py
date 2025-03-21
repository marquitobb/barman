# TODO: Uncomment after testing
# import RPi.GPIO as GPIO
import time

class RelayController:
    def __init__(self, relay_pin_one, relay_pin_two):
        self.relay_pin_one = relay_pin_one
        self.relay_pin_two = relay_pin_two
        # TODO: Uncomment after testing
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.relay_pin_one, GPIO.OUT)
        # GPIO.setup(self.relay_pin_two, GPIO.OUT)

    def turn_on_relay_one(self, duration):
        # TODO: Uncomment after testing
        # GPIO.output(self.relay_pin_one, GPIO.LOW)
        print(f"Relay one turned on... {duration} seconds")
        time.sleep(duration)
        # GPIO.output(self.relay_pin_one, GPIO.HIGH)
        print("Relay one turned off")

    def turn_on_relay_two(self, duration):
        # TODO: Uncomment after testing
        # GPIO.output(self.relay_pin_two, GPIO.LOW)
        print(f"Relay two turned on... {duration} seconds")
        time.sleep(duration)
        # GPIO.output(self.relay_pin_two, GPIO.HIGH)
        print("Relay two turned off")

    def cleanup(self):
        # TODO: Uncomment after testing
        # GPIO.cleanup()
        print("GPIO cleanup complete")

# if __name__ == "__main__":
#     relay_controller = RelayController(
#         relay_pin_one=17,  # GPIO17
#         relay_pin_two=27   # GPIO27
#     )
#     try:
#         relay_controller.turn_on_relay_one(
#             duration=5
#         )
#         relay_controller.turn_on_relay_two(
#             duration=5
#         )
#     finally:
#         relay_controller.cleanup()