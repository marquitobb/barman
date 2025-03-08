import pvporcupine
import sounddevice as sd
import numpy as np
import threading
import time
import requests
import json
from vosk import Model, KaldiRecognizer

class VoiceAssistant:
    def __init__(self, 
                 keyword="barman", 
                 sensitivity=0.5, 
                 api_url="http://localhost:8000"):
        self.keyword = keyword
        self.sensitivity = sensitivity
        self.api_url = api_url
        self.porcupine = None
        self.stream = None
        self.is_listening = False
        self.active = False
        self.vosk_model = None
        self.recognizer = None
        
    def initialize(self):
        """Inicializa el detector de palabra clave y Vosk."""
        try:
            # Inicializa Porcupine para detección de palabra clave (API actualizada)
            self.porcupine = pvporcupine.Porcupine(
                access_key="TU_CLAVE_DE_ACCESO",  # Regístrate en console.picovoice.ai
                keywords=["barman"],
                sensitivities=[self.sensitivity]
            )
            
            # Cargar modelo Vosk (modelo ligero para español)
            print("Cargando modelo de Vosk...")
            self.vosk_model = Model(model_path="vosk-model-small-es")
            self.recognizer = KaldiRecognizer(self.vosk_model, 16000)
            print("Modelo de Vosk cargado.")
            
            print(f"Asistente de voz inicializado. Palabra clave: '{self.keyword}'")
            return True
        except Exception as e:
            print(f"Error al inicializar el asistente de voz: {str(e)}")
            return False
    
    def listen_for_wake_word(self):
        """Escucha continuamente la palabra clave."""
        if not self.porcupine:
            print("El detector de palabra clave no está inicializado.")
            return
        
        self.is_listening = True
        print(f"Escuchando... Di '{self.keyword}' para activarme.")
        
        # Configura el stream de audio para porcupine
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Error de audio: {status}")
                return
            
            # Convierte a formato esperado por Porcupine
            pcm = indata.flatten().astype(np.int16)
            
            # Procesa con Porcupine
            keyword_index = self.porcupine.process(pcm)
            
            if keyword_index >= 0:
                print(f"¡'{self.keyword}' detectado!")
                # Necesitamos manejar esto en otro hilo para no bloquear el callback
                threading.Thread(target=self.on_wake_word_detected).start()
        
        try:
            # Inicia el stream
            with sd.InputStream(samplerate=self.porcupine.sample_rate,
                              blocksize=self.porcupine.frame_length,
                              dtype=np.int16, 
                              channels=1,
                              callback=audio_callback):
                while self.is_listening:
                    time.sleep(0.1)
        except Exception as e:
            print(f"Error en la escucha: {str(e)}")
        finally:
            self.is_listening = False
    
    def record_and_transcribe(self, duration=5):
        """Graba audio y lo transcribe usando Vosk."""
        print(f"Escuchando por {duration} segundos...")
        
        # Reinicia el recognizer para nueva grabación
        self.recognizer = KaldiRecognizer(self.vosk_model, 16000)
        
        text = ""
        
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Error: {status}")
            
            # Procesa el audio con Vosk
            if self.recognizer.AcceptWaveform(indata.tobytes()):
                result = json.loads(self.recognizer.Result())
                nonlocal text
                if result.get("text", ""):
                    text = result.get("text", "")
        
        # Graba audio para procesar con Vosk
        with sd.InputStream(samplerate=16000, 
                          channels=1,
                          dtype=np.int16,
                          blocksize=8000,
                          callback=audio_callback):
            time.sleep(duration)
        
        # Obtener el resultado final
        final_result = json.loads(self.recognizer.FinalResult())
        if final_result.get("text", ""):
            text = final_result.get("text", "")
        
        return text
    
    def on_wake_word_detected(self):
        """Acciones a realizar cuando se detecta la palabra clave."""
        if self.active:  # Evitar activaciones múltiples
            return
            
        self.active = True
        
        print("¿Qué deseas tomar?")
        
        # Grabar y transcribir con Vosk
        transcription = self.record_and_transcribe(duration=5)
        
        if transcription:
            print(f"Entendí: '{transcription}'")
            
            # Envía el texto a tu API
            try:
                response = requests.post(
                    f"{self.api_url}/process_command",
                    json={"command": transcription}
                )
                if response.status_code == 200:
                    print(f"Respuesta: {response.json()}")
                else:
                    print(f"Error del servidor: {response.status_code}")
            except Exception as e:
                print(f"Error al comunicarse con la API: {str(e)}")
        else:
            print("No entendí lo que dijiste.")
        
        self.active = False
        
    def start(self):
        """Inicia el asistente de voz en un hilo separado."""
        if self.initialize():
            self.thread = threading.Thread(target=self.listen_for_wake_word)
            self.thread.daemon = True
            self.thread.start()
    
    def stop_listening(self):
        """Detiene la escucha y libera recursos."""
        self.is_listening = False
        
        if self.porcupine:
            self.porcupine.delete()
            self.porcupine = None
        
        # Vosk y sounddevice liberan recursos automáticamente
        
        print("Asistente de voz detenido.")

# Función para integrar con el resto de tu sistema
def setup_voice_assistant():
    assistant = VoiceAssistant(keyword="barman")
    assistant.start()
    return assistant

# Para pruebas
if __name__ == "__main__":
    assistant = setup_voice_assistant()
    try:
        print("Asistente iniciado. Presiona Ctrl+C para salir.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Deteniendo asistente...")
    finally:
        assistant.stop_listening()