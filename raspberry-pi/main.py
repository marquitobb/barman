# voice
import sys
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

def init_barman(voice_handler):
    print("Iniciando el asistente de voz...")
    print("Di 'barman' para activar el asistente.")

    while True:
        try:
            audio = voice_handler.listen_audio(phrase_limit=3)
            if audio is None:
                print("No se pudo capturar audio. Usando alternativas...")
                # Puedes implementar un modo alternativo aquí, como usar texto predefinido
                processor = VoiceTextProcessor()
                processor.text_to_speech_spanish("No puedo escucharte, necesitas conectar un micrófono USB.", voice_name="Spanish")
                continue
            text = voice_handler.recognize_speech(audio)

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

def main():
    use_simple_voice = "--simple" in sys.argv
    
    if use_simple_voice:
        from voice.voice_commands_simple import SimpleVoiceCommands
        voice_handler = SimpleVoiceCommands()
    else:
        from voice.voice_commands import VoiceCommands
        voice_handler = VoiceCommands()
    
    init_barman(voice_handler)

# main
if __name__ == "__main__":
    main()

