"""
Simple Voice Input Processor

Since pyaudio has installation issues, this provides alternative approaches:
1. File-based voice input (upload audio files)
2. Simulation mode for testing
3. Instructions for setting up voice recording
"""

import os
from pathlib import Path
from typing import Optional

class SimpleVoiceProcessor:
    """
    Simplified voice processor that can handle file-based input
    and provides fallback options when microphone isn't available.
    """
    
    def __init__(self):
        self.audio_dir = Path("audio_input")
        self.audio_dir.mkdir(exist_ok=True)
        
    def process_audio_file(self, audio_file_path: str) -> str:
        """
        Process an audio file and convert to text.
        
        This is a placeholder - in a real implementation you would use:
        - OpenAI Whisper API
        - Google Speech-to-Text
        - Azure Speech Services
        - Local Whisper model
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            str: Transcribed text
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
        # Simulate transcription for demo
        filename = os.path.basename(audio_file_path).lower()
        
        # Mock transcriptions based on filename patterns
        mock_transcriptions = {
            "restaurant": "I had an amazing dinner at this place. The food was delicious, service was great, and the atmosphere was perfect for a date night.",
            "coffee": "Visited this coffee shop this morning. The coffee was good but a bit expensive. Staff was friendly though.",
            "repair": "Took my laptop here for repair. They fixed it quickly and the price was reasonable. Very professional service.",
            "hotel": "Stayed here for three nights. Clean rooms, good location, but the wifi was slow and breakfast could be better."
        }
        
        # Try to match filename to mock transcription
        for keyword, transcription in mock_transcriptions.items():
            if keyword in filename:
                print(f"🎤 Transcribed from {filename}: {transcription[:50]}...")
                return transcription
        
        # Default mock transcription
        default_text = "This was a good experience overall. I would recommend this place to others."
        print(f"🎤 Transcribed from {filename}: {default_text}")
        return default_text
    
    def record_voice_simulation(self) -> str:
        """
        Simulate voice recording by prompting user for text input.
        This can be used when actual voice recording isn't available.
        """
        print("🎤 Voice Recording Simulation")
        print("Since voice recording isn't set up, please type your experience:")
        experience = input("Your experience: ")
        
        if not experience.strip():
            experience = "Had a great experience at this business. Would visit again."
        
        return experience
    
    def save_transcription(self, text: str, filename: str = None) -> str:
        """Save transcription to a file for records."""
        if not filename:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transcription_{timestamp}.txt"
        
        filepath = self.audio_dir / filename
        with open(filepath, 'w') as f:
            f.write(text)
        
        return str(filepath)
    
    def get_voice_input_instructions(self) -> str:
        """
        Provide instructions for setting up real voice input.
        """
        instructions = """
        🎤 Setting up Voice Input:
        
        For real voice recording, you can:
        
        1. **Use OpenAI Whisper API** (Easiest):
           - Add OPENAI_API_KEY to your .env file
           - Record audio with any app, save as .mp3/.wav
           - Use the process_audio_file() function
        
        2. **Install local dependencies**:
           ```bash
           # On Ubuntu/Debian:
           sudo apt-get install portaudio19-dev
           pip install pyaudio SpeechRecognition
           
           # On macOS:
           brew install portaudio
           pip install pyaudio SpeechRecognition
           
           # On Windows:
           pip install pyaudio SpeechRecognition
           ```
        
        3. **Use phone recording**:
           - Record voice memo on your phone
           - Transfer to computer
           - Process with process_audio_file()
        
        4. **Online tools**:
           - Use online speech-to-text tools
           - Copy/paste the result
        """
        
        return instructions

# Example usage function
def demo_voice_input():
    """Demonstrate voice input processing."""
    processor = SimpleVoiceProcessor()
    
    print("🎤 Voice Input Demo")
    print("=" * 30)
    
    # Method 1: File-based (if audio files exist)
    audio_files = list(processor.audio_dir.glob("*.wav")) + list(processor.audio_dir.glob("*.mp3"))
    
    if audio_files:
        print("📁 Found audio files:")
        for i, file in enumerate(audio_files, 1):
            print(f"  {i}. {file.name}")
        
        try:
            choice = int(input("Select file number (or 0 for text input): "))
            if 1 <= choice <= len(audio_files):
                selected_file = audio_files[choice - 1]
                transcription = processor.process_audio_file(str(selected_file))
                processor.save_transcription(transcription)
                return transcription
        except (ValueError, IndexError):
            pass
    
    # Method 2: Text simulation
    print("No audio files found or invalid selection.")
    transcription = processor.record_voice_simulation()
    processor.save_transcription(transcription)
    
    return transcription

if __name__ == "__main__":
    demo_voice_input()