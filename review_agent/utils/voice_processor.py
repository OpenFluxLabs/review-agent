import speech_recognition as sr
from pathlib import Path

class VoiceProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def record_audio(self, duration: int = 10) -> str:
        """
        Record audio for the specified duration.
        
        Args:
            duration (int): Recording duration in seconds
            
        Returns:
            str: Path to the saved audio file
        """
        with sr.Microphone() as source:
            print("Recording... Speak now!")
            audio = self.recognizer.listen(source, timeout=duration)
            
            # Save the audio to a temporary file
            audio_file = str(Path.cwd() / "temp_recording.wav")
            with open(audio_file, "wb") as f:
                f.write(audio.get_wav_data())
            
            return audio_file

    def transcribe_audio(self, audio_file: str) -> str:
        """
        Transcribe the audio file to text.
        
        Args:
            audio_file (str): Path to the audio file
            
        Returns:
            str: Transcribed text
        """
        with sr.AudioFile(audio_file) as source:
            audio = self.recognizer.record(source)
            
        try:
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            raise ValueError("Could not understand the audio")
        except sr.RequestError:
            raise ConnectionError("Could not connect to the speech recognition service")