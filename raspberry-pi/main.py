# voice
from voice.voice_commands import VoiceCommands
from voice.voice_text import VoiceTextProcessor

# controllers
from controllers.motor_controller import MotorController

# importar el cliente API
from api.client import ApiClient
import json

# Inicializar el cliente de API
api_client = ApiClient()

# init motor controller
motor_controller = MotorController()

def process_drink_request(
    text: str
) -> str:
    response = api_client.process_drink_request(text)

    if not response or not response.get("success"):
        print("Error al procesar la solicitud de bebida")
        return None

    if not motor_controller.process_drink_request(
        text=response
    ):
        return "hubo un error al procesar la solicitud de bebida"

    return response

def init_barman():
    print("Iniciando el asistente de voz...")
    print("Di 'barman' para activar el asistente.")

    while True:
        try:
            # Initialize the voice commands
            voice_commands = VoiceCommands()
            audio = voice_commands.listen_audio(phrase_limit=3)
            text = voice_commands.recognize_speech(audio)

            # validate the keyword voice
            if text and any(keyword in text for keyword in ["barman", "bar man", "batman"]):
                processor = VoiceTextProcessor()
                processor.text_to_speech_spanish("¡Hola! ¿En qué puedo ayudarte?", voice_name="Spanish")
                processor.record_audio()
                text_from_audio = processor.transcribe_audio(processor.output_file)
                print(f"Texto: {text_from_audio}")

                # Enviar el texto transcrito a la API
                drink_data = process_drink_request(text_from_audio)

                if drink_data:
                    message_response = f"Preparando {drink_data['name']}. {drink_data['description']}"
                    processor.text_to_speech_spanish(message_response, voice_name="Spanish")
                else:
                    processor.text_to_speech_spanish("Lo siento, no pude procesar tu solicitud.", voice_name="Spanish")

                print("\n¡Palabra clave detectada!")
                print("fin...")
                break

        except KeyboardInterrupt:
            print("\nPrograma finalizado.")
            break
        except Exception as e:
            print(f"Error: {e}")

# main
if __name__ == "__main__":
    # Initialize the voice commands
    # TODO: descoment after testing
    # init_barman()
    drink_data = process_drink_request("quiero una margarita")
    print(drink_data)

