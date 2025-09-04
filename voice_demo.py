import os
from dotenv import load_dotenv
from review_agent.agent import ReviewAgent, ReviewInput
from review_agent.platforms.mock import MockPlatform
from review_agent.utils.simple_voice import SimpleVoiceProcessor

def voice_demo():
    """Demonstrate the review agent with voice input."""
    print("🎤 Review Agent - Voice Input Demo!")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Initialize voice processor
    voice_processor = SimpleVoiceProcessor()
    
    # Check if OpenAI API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  No OpenAI API key found. Using mock review generator...")
        use_ai = False
    else:
        print("✅ OpenAI API key found. Using AI review generation...")
        use_ai = True
    
    print("\n🎤 Voice Input Instructions:")
    print(voice_processor.get_voice_input_instructions())
    
    # Get business details
    print("\n📝 Business Information:")
    business_name = input("Business name: ")
    location = input("Location (optional): ")
    
    while True:
        try:
            rating = int(input("Rating (1-5): "))
            if 1 <= rating <= 5:
                break
            else:
                print("Please enter a rating between 1 and 5")
        except ValueError:
            print("Please enter a valid number")
    
    # Get voice input for experience
    print("\n🎤 Now let's get your experience...")
    print("You can either:")
    print("1. Type your experience")
    print("2. Process an audio file (if you have one)")
    
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == "2":
        # Try to process audio file
        try:
            from pathlib import Path
            audio_dir = Path("audio_input")
            audio_files = list(audio_dir.glob("*.wav")) + list(audio_dir.glob("*.mp3"))
            
            if audio_files:
                print("\n📁 Available audio files:")
                for i, file in enumerate(audio_files, 1):
                    print(f"  {i}. {file.name}")
                
                file_choice = int(input("Select file number: "))
                if 1 <= file_choice <= len(audio_files):
                    selected_file = audio_files[file_choice - 1]
                    experience_text = voice_processor.process_audio_file(str(selected_file))
                else:
                    print("Invalid selection, falling back to text input...")
                    experience_text = voice_processor.record_voice_simulation()
            else:
                print("No audio files found in audio_input/ directory")
                print("You can add .wav or .mp3 files there and try again.")
                experience_text = voice_processor.record_voice_simulation()
                
        except (ValueError, FileNotFoundError):
            print("Error processing audio, falling back to text input...")
            experience_text = voice_processor.record_voice_simulation()
    else:
        # Text input
        experience_text = voice_processor.record_voice_simulation()
    
    # Create review input
    review_input = ReviewInput(
        business_name=business_name,
        experience_text=experience_text,
        rating=rating,
        visit_date="2024-03-21"
    )
    
    print("\n🤖 Generating review from your voice input...")
    
    if use_ai:
        try:
            # Initialize the review agent with AI
            agent = ReviewAgent(api_key=api_key)
            review = agent.generate_review(review_input)
        except Exception as e:
            print(f"AI generation failed: {e}")
            review = generate_fallback_review(review_input)
    else:
        # Use a simple template for mock
        review = generate_fallback_review(review_input)
    
    print("\n📝 Generated Review:")
    print("=" * 50)
    print(review)
    print("=" * 50)
    
    # Ask user if they want to post
    post_review = input("\nWould you like to post this review? (y/n): ").lower() == 'y'
    
    if post_review:
        # Initialize platforms
        platforms = [
            MockPlatform("Google Reviews"),
            MockPlatform("Yelp"),
            MockPlatform("TripAdvisor")
        ]
        
        print(f"\n📤 Posting to {len(platforms)} platforms...")
        
        for platform in platforms:
            print(f"\n📤 Posting to {platform.platform_name}...")
            
            # Login (mock)
            platform.login({"username": "demo", "password": "demo"})
            
            # Search business (mock)
            business_id = platform.search_business(
                review_input.business_name, 
                location
            )
            
            # Post review (mock)
            result = platform.post_review(business_id, review, review_input.rating)
            
        print(f"\n🎉 Voice-to-review process complete!")
        print("📁 Check the 'mock_reviews' folder to see your generated review.")
        
        # Save the transcription
        transcription_file = voice_processor.save_transcription(
            experience_text, 
            f"{business_name.replace(' ', '_').lower()}_transcription.txt"
        )
        print(f"💾 Voice transcription saved to: {transcription_file}")
        
    else:
        print("\n👍 Review generated but not posted. Thanks for trying the voice demo!")

def generate_fallback_review(review_input: ReviewInput) -> str:
    """Generate a simple review without AI."""
    rating_text = {
        5: "Excellent experience!",
        4: "Very good experience.",
        3: "Good experience overall.",
        2: "Okay experience, could be better.",
        1: "Poor experience."
    }
    
    review = f"I visited {review_input.business_name} and {review_input.experience_text} "
    review += f"{rating_text.get(review_input.rating, 'Had an experience.')} "
    review += f"I would rate this {review_input.rating} out of 5 stars."
    
    if review_input.rating >= 4:
        review += " Highly recommended!"
    elif review_input.rating <= 2:
        review += " Hope they can improve."
    
    return review

if __name__ == "__main__":
    voice_demo()