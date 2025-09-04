import os
from dotenv import load_dotenv
from review_agent.agent import ReviewAgent, ReviewInput
from review_agent.platforms.mock import MockPlatform
from review_agent.platforms.local_directory import LocalDirectoryPlatform

def demo_review_agent():
    """Demonstrate the review agent with sample data."""
    print("🎤 Review Agent MVP - Demo Mode!")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if OpenAI API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  No OpenAI API key found. Using mock review generator...")
        use_ai = False
    else:
        print("✅ OpenAI API key found. Using AI review generation...")
        use_ai = True
    
    # Sample review data
    sample_reviews = [
        {
            'business_name': "Mario's Italian Bistro",
            'experience_text': "Amazing pasta, friendly staff, cozy atmosphere. The tiramisu was incredible!",
            'rating': 5,
            'visit_date': "2024-03-15"
        },
        {
            'business_name': "TechFix Computer Repair",
            'experience_text': "Fixed my laptop quickly and at a fair price. Very knowledgeable technician.",
            'rating': 4,
            'visit_date': "2024-03-18"
        }
    ]
    
    for i, sample in enumerate(sample_reviews, 1):
        print(f"\n🔄 Processing Review {i}/{len(sample_reviews)}...")
        print(f"Business: {sample['business_name']}")
        print(f"Experience: {sample['experience_text']}")
        print(f"Rating: {sample['rating']}/5")
        
        # Create review input
        review_input = ReviewInput(
            business_name=sample['business_name'],
            experience_text=sample['experience_text'],
            rating=sample['rating'],
            visit_date=sample['visit_date']
        )
        
        print("\n🤖 Generating review...")
        
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
        print("-" * 40)
        print(review)
        print("-" * 40)
        
        # Initialize platforms (mix of mock and semi-real)
        platforms = [
            MockPlatform("Google Reviews"),
            MockPlatform("Yelp"),
            LocalDirectoryPlatform()  # This one tries to make real API calls
        ]
        
        print(f"\n📤 Posting to {len(platforms)} platforms...")
        
        for platform in platforms:
            platform_name = getattr(platform, 'platform_name', platform.__class__.__name__)
            print(f"\n📤 Posting to {platform_name}...")
            
            # Login
            if isinstance(platform, LocalDirectoryPlatform):
                platform.login({"api_key": "demo_key"})
            else:
                platform.login({"username": "demo", "password": "demo"})
            
            # Search business
            business_id = platform.search_business(
                review_input.business_name, 
                "New York"  # Adding location for more realistic demo
            )
            
            # Post review
            result = platform.post_review(business_id, review, review_input.rating)
        
        print(f"✅ Review {i} posted successfully!\n")
    
    print("🎉 Demo complete! Reviews have been posted to multiple platforms.")
    print("📁 Check the 'mock_reviews' folder to see your generated reviews.")
    print("\n💡 Next steps:")
    print("   - Add your OpenAI API key to .env for AI-generated reviews")
    print("   - Run a local directory server for real API testing")
    print("   - Add voice input functionality")
    print("   - Integrate with real review platforms")
    
    return True

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
    demo_review_agent()