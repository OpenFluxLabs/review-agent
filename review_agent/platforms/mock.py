import json
import os
from datetime import datetime
from typing import Dict, Any
from .base import ReviewPlatform

class MockPlatform(ReviewPlatform):
    """
    Mock platform for testing and development.
    Saves reviews to local files instead of posting online.
    """
    
    def __init__(self, platform_name: str = "Mock"):
        self.platform_name = platform_name
        self.reviews_dir = "mock_reviews"
        self.is_logged_in = False
        
        # Create reviews directory if it doesn't exist
        os.makedirs(self.reviews_dir, exist_ok=True)

    def login(self, credentials: Dict[str, str]):
        """
        Mock login - always succeeds.
        
        Args:
            credentials: Any credentials (ignored in mock)
        """
        print(f"✅ Mock login successful to {self.platform_name}")
        self.is_logged_in = True
        return True

    def search_business(self, business_name: str, location: str = None) -> str:
        """
        Mock business search - returns a mock business ID.
        
        Args:
            business_name: Name of the business
            location: Optional location
            
        Returns:
            str: Mock business ID
        """
        if not self.is_logged_in:
            raise ValueError("Must be logged in to search businesses")
            
        # Create a simple ID from business name
        business_id = business_name.lower().replace(" ", "_").replace(",", "")
        if location:
            business_id += f"_{location.lower().replace(' ', '_')}"
            
        print(f"🔍 Found business: {business_name} (ID: {business_id})")
        return business_id

    def post_review(self, business_id: str, review_text: str, rating: int):
        """
        Mock review posting - saves to local file.
        
        Args:
            business_id: Business identifier
            review_text: Review content
            rating: Rating 1-5
        """
        if not self.is_logged_in:
            raise ValueError("Must be logged in to post reviews")
            
        timestamp = datetime.now().isoformat()
        
        review_data = {
            'platform': self.platform_name,
            'business_id': business_id,
            'review_text': review_text,
            'rating': rating,
            'timestamp': timestamp,
            'status': 'posted_successfully'
        }
        
        # Save to file
        filename = f"{self.reviews_dir}/{business_id}_{timestamp.replace(':', '-')}.json"
        with open(filename, 'w') as f:
            json.dump(review_data, f, indent=2)
            
        print(f"✅ Review posted successfully to {self.platform_name}")
        print(f"📁 Saved to: {filename}")
        print(f"⭐ Rating: {rating}/5")
        print(f"📝 Preview: {review_text[:100]}...")
        
        return review_data

    def get_all_reviews(self) -> list:
        """Get all posted reviews from files."""
        reviews = []
        
        for filename in os.listdir(self.reviews_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.reviews_dir, filename), 'r') as f:
                    reviews.append(json.load(f))
                    
        return sorted(reviews, key=lambda x: x['timestamp'], reverse=True)