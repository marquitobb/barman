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
        self.available_devices = self._list_audio_devices()

    def _list_audio_devices(self):
        """Listar todos los dispositivos de audio disponibles"""
        devices = []
        try:
            print("Dispositivos de micrófono disponibles:")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"Índice {index}: {name}")
                # Priorizar el micrófono Razer Seiren Mini
                if "Razer Seiren Mini" in name:
                    print(f"¡Encontrado Razer Seiren Mini en índice {index}!")
                    return [index]  # Devolver solo este dispositivo
                devices.append(index)
            return devices
        except Exception as e:
            print(f"Error al listar dispositivos: {e}")
            return []

    def try_get_microphone(self):
        """Intenta obtener un micrófono funcionando"""
        if not self.available_devices:
            print("No se encontraron dispositivos de micrófono")
            return None
            
        # Probar el dispositivo USB si está disponible (suele ser más confiable)
        for index in self.available_devices:
            try:
                print(f"Intentando usar dispositivo {index}...")
                mic = sr.Microphone(device_index=index)
                # Probar si el dispositivo funciona realmente
                with mic as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=1)
                print(f"Dispositivo {index} funciona correctamente")
                return index
            except Exception as e:
                print(f"Error con dispositivo {index}: {e}")
                continue
                
        return None

    def listen_audio(self, timeout=None, phrase_limit=None):
        """Función auxiliar para escuchar audio del micrófono"""
        # Intentar obtener un dispositivo que funcione
        device_index = self.try_get_microphone()
        
        if device_index is None:
            print("No se pudo encontrar un micrófono funcional. Ejecute 'arecord -l' para ver dispositivos.")
            return None
            
        try:
            with sr.Microphone(device_index=device_index) as source:
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
