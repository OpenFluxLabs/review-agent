import os
from dotenv import load_dotenv
from review_agent.agent import ReviewAgent, ReviewInput
from review_agent.platforms.mock import MockPlatform

def get_user_input():
    """Get user input for the review."""
    print("🎤 Review Agent MVP - Let's create your review!")
    print("-" * 50)
    
    business_name = input("Business name: ")
    location = input("Location (optional): ")
    
    print("\nTell us about your experience:")
    experience_text = input("Your experience: ")
    
    while True:
        try:
            rating = int(input("Rating (1-5): "))
            if 1 <= rating <= 5:
                break
            else:
                print("Please enter a rating between 1 and 5")
        except ValueError:
            print("Please enter a valid number")
    
    visit_date = input("Visit date (optional, YYYY-MM-DD): ") or None
    
    return {
        'business_name': business_name,
        'location': location,
        'experience_text': experience_text,
        'rating': rating,
        'visit_date': visit_date
    }

def main():
    # Load environment variables
    load_dotenv()
    
    # Check if OpenAI API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  No OpenAI API key found. Please set OPENAI_API_KEY in your .env file")
        print("For now, we'll use a mock review generator...")
        use_ai = False
    else:
        use_ai = True
    
    # Get user input
    user_input = get_user_input()
    
    # Create review input
    review_input = ReviewInput(
        business_name=user_input['business_name'],
        experience_text=user_input['experience_text'],
        rating=user_input['rating'],
        visit_date=user_input['visit_date']
    )
    
    print("\n🤖 Generating review...")
    
    if use_ai:
        # Initialize the review agent with AI
        agent = ReviewAgent(api_key=api_key)
        review = agent.generate_review(review_input)
    else:
        # Use a simple template for mock
        review = f"""I visited {review_input.business_name} and had this experience: {review_input.experience_text}
        
Overall, I would rate this {review_input.rating} out of 5 stars. {"Highly recommended!" if review_input.rating >= 4 else "Could be better." if review_input.rating >= 3 else "Not recommended."}"""
    
    print("\n📝 Generated Review:")
    print("=" * 50)
    print(review)
    print("=" * 50)
    
    # Ask user if they want to post
    post_review = input("\nWould you like to post this review? (y/n): ").lower() == 'y'
    
    if post_review:
        # Initialize mock platforms
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
            business_id = platform.search_business(
                review_input.business_name, 
                user_input.get('location')
            )
            
            # Post review (mock)
            result = platform.post_review(business_id, review, review_input.rating)
            
        print(f"\n🎉 All done! Your reviews have been 'posted' to {len(platforms)} platforms.")
        print("📁 Check the 'mock_reviews' folder to see your generated reviews.")
    else:
        print("\n👍 Review generated but not posted. Thanks for trying the MVP!")

if __name__ == "__main__":
    main()