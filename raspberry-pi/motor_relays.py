import RPi.GPIO as GPIO
import time

class RelayController:
    def __init__(self):
        # No inicializamos pines aquí para mantenerlos completamente independientes
        print("Controlador de relés inicializado")

    def operate_relay_one(self, pin, duration):
        try:
            # Configuración específica para el relé 1
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            
            # Asegurar que inicie apagado
            GPIO.output(pin, GPIO.HIGH)
            print(f"Relé 1 (pin {pin}) inicializado")
            time.sleep(1)  # Estabilización
            
            # Activar relé 1
            GPIO.output(pin, GPIO.LOW)
            print("Relé 1 encendido")
            time.sleep(duration)
            
            # Desactivar relé 1
            GPIO.output(pin, GPIO.HIGH)
            print("Relé 1 apagado")
            
        finally:
            # Limpieza específica del relé 1
            GPIO.cleanup(pin)
            print("Recursos del relé 1 liberados")
            
        # Espera completa entre operaciones
        time.sleep(2)

    def operate_relay_two(self, pin, duration):
        try:
            # Configuración específica para el relé 2
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            
            # Asegurar que inicie apagado
            GPIO.output(pin, GPIO.HIGH)
            print(f"Relé 2 (pin {pin}) inicializado")
            time.sleep(1)  # Estabilización
            
            # Activar relé 2
            GPIO.output(pin, GPIO.LOW)
            print("Relé 2 encendido")
            time.sleep(duration)
            
            # Desactivar relé 2
            GPIO.output(pin, GPIO.HIGH)
            print("Relé 2 apagado")
            
        finally:
            # Limpieza específica del relé 2
            GPIO.cleanup(pin)
            print("Recursos del relé 2 liberados")

if __name__ == "__main__":
    relay_controller = RelayController()
    try:
        # Operar cada relé por separado con su propio ciclo completo
        print("\n--- Iniciando secuencia del relé 1 ---")
        relay_controller.operate_relay_one(pin=20, duration=7)
        
        print("\n--- Iniciando secuencia del relé 2 ---")
        relay_controller.operate_relay_two(pin=17, duration=7)
        
    except KeyboardInterrupt:
        print("\nOperación interrumpida por el usuario")
        # Asegurar limpieza general
        GPIO.cleanup()
    except Exception as e:
        print(f"\nError: {e}")
        GPIO.cleanup()