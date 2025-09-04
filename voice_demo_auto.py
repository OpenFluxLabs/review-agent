import os
from dotenv import load_dotenv
from review_agent.agent import ReviewAgent, ReviewInput
from review_agent.platforms.mock import MockPlatform
from review_agent.utils.simple_voice import SimpleVoiceProcessor

def voice_demo_auto():
    """Automatic voice demo without user input."""
    print("🎤 Review Agent - Voice Input Demo (Auto Mode)!")
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
    
    # Sample business and experience
    business_name = "Mario's Italian Restaurant"
    location = "New York"
    rating = 5
    
    print(f"\n📝 Business: {business_name}")
    print(f"📍 Location: {location}")
    print(f"⭐ Rating: {rating}/5")
    
    # Simulate processing an audio file
    print("\n🎤 Processing voice input...")
    
    # Check if we have an audio file to process
    audio_file = "audio_input/restaurant_review.wav"
    if os.path.exists(audio_file):
        experience_text = voice_processor.process_audio_file(audio_file)
    else:
        # Use simulated voice input
        experience_text = "I had an amazing dinner at this restaurant. The pasta was perfectly cooked, the sauce was incredible, and our server was very attentive. The atmosphere was romantic and perfect for our anniversary dinner. Definitely coming back!"
        print(f"🎤 Simulated voice transcription: {experience_text[:50]}...")
    
    # Create review input
    review_input = ReviewInput(
        business_name=business_name,
        experience_text=experience_text,
        rating=rating,
        visit_date="2024-03-21"
    )
    
    print("\n🤖 Generating review from voice input...")
    
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
    
    print("\n📝 Generated Review from Voice:")
    print("=" * 50)
    print(review)
    print("=" * 50)
    
    # Auto-post the review
    print("\n📤 Auto-posting review to platforms...")
    
    # Initialize platforms
    platforms = [
        MockPlatform("Google Reviews"),
        MockPlatform("Yelp"),
        MockPlatform("TripAdvisor")
    ]
    
    for platform in platforms:
        print(f"\n📤 Posting to {platform.platform_name}...")
        
        # Login (mock)
        platform.login({"username": "demo", "password": "demo"})
        
        # Search business (mock)
        business_id = platform.search_business(business_name, location)
        
        # Post review (mock)
        result = platform.post_review(business_id, review, rating)
    
    print(f"\n🎉 Voice-to-review process complete!")
    print("📁 Check the 'mock_reviews' folder to see your generated review.")
    
    # Save the transcription
    transcription_file = voice_processor.save_transcription(
        experience_text, 
        f"{business_name.replace(' ', '_').lower()}_voice_transcription.txt"
    )
    print(f"💾 Voice transcription saved to: {transcription_file}")
    
    print(f"\n✨ Summary:")
    print(f"   🎤 Voice Input: {experience_text[:60]}...")
    print(f"   🤖 AI Generated: {len(review)} character review")
    print(f"   📤 Posted to: {len(platforms)} platforms")
    print(f"   ⭐ Rating: {rating}/5 stars")

def generate_fallback_review(review_input: ReviewInput) -> str:
    """Generate a simple review without AI."""
    rating_text = {
        5: "Excellent experience!",
        4: "Very good experience.",
        3: "Good experience overall.",
        2: "Okay experience, could be better.",
        1: "Poor experience."
    }
    
    review = f"I visited {review_input.business_name} and had this to say: {review_input.experience_text} "
    review += f"{rating_text.get(review_input.rating, 'Had an experience.')} "
    review += f"I would rate this {review_input.rating} out of 5 stars."
    
    if review_input.rating >= 4:
        review += " Highly recommended!"
    elif review_input.rating <= 2:
        review += " Hope they can improve."
    
    return review

if __name__ == "__main__":
    voice_demo_auto()