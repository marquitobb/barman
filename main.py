import RPi.GPIO as GPIO
import time

# Configurar el modo de numeración de los pines
GPIO.setmode(GPIO.BCM)

# Definir el pin GPIO al que está conectado el relay
relay_pin = 21 # or pin 40
relay_pin_two = 20 # or pin 38

# Configurar el pin como salida
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(relay_pin_two, GPIO.OUT)

try:
    # Encender el relay
    GPIO.output(relay_pin, GPIO.LOW)
    GPIO.output(relay_pin_two, GPIO.LOW)
    print("Relay encendido")
    time.sleep(10)  # Mantener el relay encendido por 5 segundos

    # Apagar el relay
    GPIO.output(relay_pin, GPIO.HIGH)
    GPIO.output(relay_pin_two, GPIO.HIGH)
    print("Relay apagado")
finally:
    # Limpiar la configuración de los pines GPIO
    GPIO.cleanup()