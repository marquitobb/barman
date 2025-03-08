import speech_recognition as sr

class VoiceCommands:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen_audio(self, timeout=None, phrase_limit=None):
        """Función auxiliar para escuchar audio del micrófono"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            return self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

    def recognize_speech(self, audio):
        """Función auxiliar para reconocer el habla"""
        try:
            return self.recognizer.recognize_google(audio, language="es-ES").lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Error en la API de reconocimiento: {e}")
            return None
