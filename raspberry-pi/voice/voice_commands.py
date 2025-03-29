import pyaudio
import speech_recognition as sr
import time
import os

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
            # Implementación alternativa directamente con PyAudio para evitar errores
            audio_data = self._record_with_pyaudio(duration=5 if phrase_limit is None else phrase_limit)
            if audio_data:
                with open("temp_recording.wav", "wb") as f:
                    f.write(audio_data)
                with sr.AudioFile("temp_recording.wav") as source:
                    return self.recognizer.record(source)
            return None
        except Exception as e:
            print(f"Error al escuchar audio: {e}")
            return None
    
    def _record_with_pyaudio(self, duration=5, rate=16000):
        """Grabación directa con PyAudio para evitar errores de ALSA"""
        try:
            import wave
            p = pyaudio.PyAudio()
            
            # Usar directamente el dispositivo correcto
            stream = p.open(
                rate=rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                input_device_index=self.device_index,
                frames_per_buffer=1024
            )
            
            print("Grabando audio...")
            frames = []
            for i in range(0, int(rate / 1024 * duration)):
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(data)
            
            print("Grabación finalizada.")
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Guardar en un archivo temporal
            wf = wave.open("temp_recording.wav", 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            with open("temp_recording.wav", "rb") as f:
                return f.read()
        except Exception as e:
            print(f"Error en grabación directa: {e}")
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
