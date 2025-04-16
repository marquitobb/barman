import RPi.GPIO as GPIO
import time

class RelayController:
    def __init__(self, relay_pin_one, relay_pin_two):
        self.relay_pin_one = relay_pin_one
        self.relay_pin_two = relay_pin_two
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.relay_pin_one, GPIO.OUT)
        GPIO.setup(self.relay_pin_two, GPIO.OUT)

    def turn_on_relay_one(self, duration):
        GPIO.output(self.relay_pin_one, GPIO.LOW)
        print("Relay one turned on")
        time.sleep(duration)
        GPIO.output(self.relay_pin_one, GPIO.HIGH)
        print("Relay one turned off")

    def turn_on_relay_two(self, duration):
        GPIO.output(self.relay_pin_two, GPIO.LOW)
        print("Relay two turned on")
        time.sleep(duration)
        GPIO.output(self.relay_pin_two, GPIO.HIGH)
        print("Relay two turned off")

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    relay_controller = RelayController(
        relay_pin_one=20,  # GPIO20
        relay_pin_two=17   # GPIO17
    )
    try:
        relay_controller.turn_on_relay_one(
            duration=7
        )
        relay_controller.turn_on_relay_two(
            duration=7
        )
    finally:
        relay_controller.cleanup()