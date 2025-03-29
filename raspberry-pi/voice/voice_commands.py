import speech_recognition as sr
import time
import os
import wave

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
            # Intenta primero usar PyAudio de forma segura
            try:
                import pyaudio
                p = pyaudio.PyAudio()
                
                # Verificar si el dispositivo existe antes de usarlo
                info = p.get_device_info_by_index(self.device_index)
                if not info.get('maxInputChannels', 0) > 0:
                    print(f"Dispositivo {self.device_index} no tiene canales de entrada")
                    p.terminate()
                    raise ValueError("Dispositivo no válido")
                
                p.terminate()
                
                # Si llegamos aquí, el dispositivo es válido, intentemos grabar
                audio_data = self._record_with_pyaudio(
                    duration=5 if phrase_limit is None else phrase_limit
                )
                
                if audio_data:
                    with open("temp_recording.wav", "wb") as f:
                        f.write(audio_data)
                    with sr.AudioFile("temp_recording.wav") as source:
                        return self.recognizer.record(source)
            except Exception as e:
                print(f"PyAudio falló, intentando alternativa: {e}")
                # Intenta usar SpeechRecognition directamente con un manejo de errores mejor
                with sr.Microphone(device_index=self.device_index) as source:
                    print("Ajustando para ruido ambiental...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("Escuchando...")
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
                    return audio
            
            return None
        except Exception as e:
            print(f"Error al escuchar audio: {e}")
            return None
    
    def _record_with_pyaudio(self, duration=5, rate=16000):
        """Grabación directa con PyAudio para evitar errores de ALSA"""
        try:
            import pyaudio
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
                try:
                    data = stream.read(1024, exception_on_overflow=False)
                    frames.append(data)
                except Exception as e:
                    print(f"Error leyendo audio: {e}")
                    break
            
            print("Grabación finalizada.")
            
            if len(frames) == 0:
                raise ValueError("No se capturó audio")
                
            try:
                stream.stop_stream()
                stream.close()
            except:
                pass
                
            try:
                p.terminate()
            except:
                pass
            
            # Guardar en un archivo temporal
            with wave.open("temp_recording.wav", 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                wf.setframerate(rate)
                wf.writeframes(b''.join(frames))
            
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
