import sounddevice as sd
from scipy.io.wavfile import write
import whisper  # Esto importará el paquete openai-whisper correcto
import pyttsx3

class VoiceTextProcessor:
    def __init__(self, sample_rate=44100, duration=5, output_file="recorded_audio.wav"):
        self.sample_rate = sample_rate
        self.duration = duration
        self.output_file = output_file

    def record_audio(self):
        print(f"Recording for {self.duration} seconds...")
        audio = sd.rec(int(self.sample_rate * self.duration), samplerate=self.sample_rate, channels=1, dtype="int16")
        sd.wait()  # Wait until the recording is finished
        write(self.output_file, self.sample_rate, audio)  # Save as WAV file
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
