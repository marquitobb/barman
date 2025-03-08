import speech_recognition as sr

# Inicializar el reconocedor de voz (una sola vez para todo el programa)
recognizer = sr.Recognizer()

def listen_audio(timeout=None, phrase_limit=None):
    """Función auxiliar para escuchar audio del micrófono"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        return recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

def recognize_speech(audio):
    """Función auxiliar para reconocer el habla"""
    try:
        return recognizer.recognize_google(audio, language="es-ES").lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Error en la API de reconocimiento: {e}")
        return None

def listen_for_keyword():
    print("Asistente iniciado. Di 'barman' para activarme...")

    while True:
        try:
            audio = listen_audio(phrase_limit=3)
            text = recognize_speech(audio)

            if text and any(keyword in text for keyword in ["barman", "bar man", "batman"]):
                print("\n¡Palabra clave detectada!")
                print("fin...")
                break

        except KeyboardInterrupt:
            print("\nPrograma finalizado.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        import pyaudio
        listen_for_keyword()
    except ImportError as e:
        print(f"Error: Falta biblioteca necesaria - {e}")
        print("Asegúrate de instalar 'SpeechRecognition' y 'PyAudio' con pip")

