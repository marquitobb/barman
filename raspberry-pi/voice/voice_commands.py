import speech_recognition as sr
import os
import time

class VoiceCommands:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Configurar mejor el reconocedor para ambientes ruidosos
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        # Usar directamente el índice 2 para Razer Seiren Mini (card 2)
        self.device_index = 2
        
    def listen_audio(self, timeout=None, phrase_limit=None):
        """Función auxiliar para escuchar audio del micrófono"""
        try:
            # Usar directamente el dispositivo específico
            with sr.Microphone(device_index=self.device_index) as source:
                print("Ajustando para ruido ambiental...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                print("Escuchando...")
                return self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        except Exception as e:
            print(f"Error al escuchar audio: {e}")
            return None

    def recognize_speech(self, audio):
        """Función auxiliar para reconocer el habla"""
        if audio is None:
            return None
            
        try:
            return self.recognizer.recognize_google(audio, language="es-ES").lower()
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
            return None
        except sr.RequestError as e:
            print(f"Error en la API de reconocimiento: {e}")
            return None
        except Exception as e:
            print(f"Error desconocido: {e}")
            return None
