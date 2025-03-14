import pyaudio
import wave
import numpy as np
import whisper
import pyttsx3

class VoiceTextProcessor:
    def __init__(self, sample_rate=44100, duration=5, output_file="recorded_audio.wav"):
        self.sample_rate = sample_rate
        self.duration = duration
        self.output_file = output_file
        self.chunk = 1024  # Tamaño de cada fragmento de audio

    def record_audio(self):
        print(f"Recording for {self.duration} seconds...")
        
        # Inicializa PyAudio
        audio = pyaudio.PyAudio()
        
        # Configura y abre el stream
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        # Graba los fragmentos de audio
        frames = []
        for i in range(0, int(self.sample_rate / self.chunk * self.duration)):
            data = stream.read(self.chunk)
            frames.append(data)
            
        # Detiene y cierra el stream
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Guarda el archivo de audio
        with wave.open(self.output_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
            
        print(f"Recording saved to {self.output_file}")

    def transcribe_audio(self, file_path):
        print("Loading Whisper model...")
        model = whisper.load_model("base")
        print("Transcribing audio...")
        result = model.transcribe(file_path)
        print("Transcription:")
        print(result["text"])
        return result["text"]

    def text_to_speech_spanish(self, text, voice_name=""):
        engine = pyttsx3.init()

        # Set a specific voice (e.g., for Spanish)
        voices = engine.getProperty("voices")
        for voice in voices:
            if voice_name.lower() in voice.name.lower():
                engine.setProperty("voice", voice.id)
                print(f"Using voice: {voice.name}")
                break
        engine.say(text)
        engine.runAndWait()

if __name__ == "__main__":
    processor = VoiceTextProcessor()
    processor.record_audio()
    text_from_audio = processor.transcribe_audio(processor.output_file)
    processor.text_to_speech_spanish(text_from_audio, voice_name="Spanish")
