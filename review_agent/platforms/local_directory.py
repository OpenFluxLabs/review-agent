import requests
import json
from typing import Dict, Any
from .base import ReviewPlatform

class LocalDirectoryPlatform(ReviewPlatform):
    """
    Local Business Directory Platform - A simple REST API platform
    that we can use for testing real review posting functionality.
    
    This simulates a real review platform but is under our control.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_key = None
        self.session = requests.Session()
        self.is_authenticated = False

    def login(self, credentials: Dict[str, str]):
        """
        Authenticate with the local directory API.
        
        Args:
            credentials: Dict containing 'api_key' or 'username'/'password'
        """
        if 'api_key' in credentials:
            self.api_key = credentials['api_key']
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
            self.is_authenticated = True
            print("✅ Local Directory API authentication successful")
            return True
        else:
            # For demo purposes, accept any credentials
            self.is_authenticated = True  
            print("✅ Local Directory login successful (demo mode)")
            return True

    def search_business(self, business_name: str, location: str = None) -> str:
        """
        Search for a business in the local directory.
        
        Args:
            business_name: Name of the business
            location: Optional location filter
            
        Returns:
            str: Business ID
        """
        if not self.is_authenticated:
            raise ValueError("Must be authenticated to search businesses")
        
        try:
            search_url = f"{self.base_url}/api/businesses/search"
            params = {
                'name': business_name,
                'location': location
            }
            
            response = self.session.get(search_url, params=params)
            
            if response.status_code == 200:
                results = response.json()
                if results.get('businesses'):
                    business = results['businesses'][0]
                    print(f"🔍 Found business: {business['name']} (ID: {business['id']})")
                    return business['id']
                else:
                    # If not found, create a new business entry
                    return self._create_business(business_name, location)
            else:
                # API not available, create mock ID
                return self._create_mock_business_id(business_name, location)
                
        except requests.exceptions.ConnectionError:
            # Local server not running, create mock ID
            return self._create_mock_business_id(business_name, location)

    def post_review(self, business_id: str, review_text: str, rating: int):
        """
        Post a review to the local directory.
        
        Args:
            business_id: Business identifier
            review_text: Review content
            rating: Rating 1-5
        """
        if not self.is_authenticated:
            raise ValueError("Must be authenticated to post reviews")
        
        try:
            review_url = f"{self.base_url}/api/businesses/{business_id}/reviews"
            
            review_data = {
                'text': review_text,
                'rating': rating,
                'author': 'Review Agent User',
                'date': '2024-03-21'
            }
            
            response = self.session.post(review_url, json=review_data)
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"✅ Review posted to Local Directory")
                print(f"📝 Review ID: {result.get('id', 'N/A')}")
                return result
            else:
                raise ValueError(f"Review posting failed: {response.text}")
                
        except requests.exceptions.ConnectionError:
            # Local server not running, simulate successful post
            return self._simulate_post(business_id, review_text, rating)

    def _create_business(self, business_name: str, location: str = None) -> str:
        """Create a new business entry in the directory."""
        try:
            create_url = f"{self.base_url}/api/businesses"
            
            business_data = {
                'name': business_name,
                'location': location or 'Unknown Location',
                'category': 'General Business'
            }
            
            response = self.session.post(create_url, json=business_data)
            
            if response.status_code in [200, 201]:
                result = response.json()
                business_id = result.get('id', self._create_mock_business_id(business_name, location))
                print(f"🆕 Created new business: {business_name} (ID: {business_id})")
                return business_id
            else:
                return self._create_mock_business_id(business_name, location)
                
        except requests.exceptions.ConnectionError:
            return self._create_mock_business_id(business_name, location)

    def _create_mock_business_id(self, business_name: str, location: str = None) -> str:
        """Create a mock business ID when API is not available."""
        base_id = business_name.lower().replace(" ", "_").replace(",", "")
        if location:
            base_id += f"_{location.lower().replace(' ', '_')}"
        
        print(f"🔍 Mock business ID created: {base_id}")
        return base_id

    def _simulate_post(self, business_id: str, review_text: str, rating: int) -> Dict[str, Any]:
        """Simulate a successful review post when API is not available."""
        result = {
            'id': f"review_{business_id}_{hash(review_text) % 10000}",
            'business_id': business_id,
            'text': review_text,
            'rating': rating,
            'status': 'posted_successfully',
            'platform': 'Local Directory (Simulated)'
        }
        
        print(f"✅ Review simulated successfully on Local Directory")
        print(f"📝 Simulated Review ID: {result['id']}")
        return result

    def get_business_reviews(self, business_id: str) -> list:
        """Get all reviews for a business."""
        try:
            reviews_url = f"{self.base_url}/api/businesses/{business_id}/reviews"
            response = self.session.get(reviews_url)
            
            if response.status_code == 200:
                return response.json().get('reviews', [])
            else:
                return []
                
        except requests.exceptions.ConnectionError:
            return []  # Return empty list if API not available