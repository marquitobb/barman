# listen the voice commands and execute the actions
from voice.voice_commands import VoiceCommands

# convert voice to text and text to voice
from voice.voice_text import VoiceTextProcessor


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
                processor.record_audio()
                text_from_audio = processor.transcribe_audio(processor.output_file)
                print(f"Texto: {text_from_audio}")
                # processor.text_to_speech_spanish(text_from_audio, voice_name="Spanish")

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
    init_barman()