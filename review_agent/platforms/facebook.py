import requests
import json
from typing import Dict, Any, Optional
from .base import ReviewPlatform

class FacebookPlatform(ReviewPlatform):
    """
    Facebook Business Platform integration.
    Uses Facebook Graph API for posting reviews/recommendations.
    
    Note: Facebook doesn't allow posting reviews directly, but allows
    posting recommendations and check-ins which can include text.
    """
    
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v18.0"
        self.access_token = None
        self.session = requests.Session()
        self.user_id = None

    def login(self, credentials: Dict[str, str]):
        """
        Authenticate with Facebook using access token.
        
        Args:
            credentials: Dict containing 'access_token'
        """
        self.access_token = credentials.get('access_token')
        if not self.access_token:
            raise ValueError("Facebook access token is required")
            
        # Test the token by getting user info
        test_url = f"{self.base_url}/me"
        params = {'access_token': self.access_token}
        
        response = self.session.get(test_url, params=params)
        
        if response.status_code == 200:
            user_data = response.json()
            self.user_id = user_data.get('id')
            print(f"✅ Facebook login successful for user: {user_data.get('name', 'Unknown')}")
            return True
        else:
            raise ValueError(f"Facebook authentication failed: {response.text}")

    def search_business(self, business_name: str, location: str = None) -> str:
        """
        Search for a business on Facebook.
        
        Args:
            business_name: Name of the business
            location: Optional location filter
            
        Returns:
            str: Facebook Page ID
        """
        if not self.access_token:
            raise ValueError("Must be logged in to search businesses")
            
        search_url = f"{self.base_url}/search"
        params = {
            'q': business_name,
            'type': 'page',
            'access_token': self.access_token,
            'fields': 'id,name,location,category'
        }
        
        if location:
            params['q'] += f" {location}"
            
        response = self.session.get(search_url, params=params)
        
        if response.status_code == 200:
            results = response.json()
            if results.get('data'):
                # Return the first match's ID
                page = results['data'][0]
                print(f"🔍 Found business: {page['name']} (ID: {page['id']})")
                return page['id']
            else:
                raise ValueError(f"No Facebook page found for: {business_name}")
        else:
            raise ValueError(f"Facebook search failed: {response.text}")

    def post_review(self, business_id: str, review_text: str, rating: int):
        """
        Post a review/recommendation to Facebook.
        
        Note: Facebook doesn't support direct review posting via API.
        This method posts a recommendation instead.
        
        Args:
            business_id: Facebook Page ID
            review_text: Review content
            rating: Rating 1-5 (converted to recommend/not recommend)
        """
        if not self.access_token:
            raise ValueError("Must be logged in to post reviews")
            
        # Facebook uses recommendations (yes/no) rather than star ratings
        recommend = rating >= 3
        
        # Post as a recommendation on the page
        post_url = f"{self.base_url}/{business_id}/recommendations"
        
        post_data = {
            'recommend': recommend,
            'review_text': review_text,
            'access_token': self.access_token
        }
        
        response = self.session.post(post_url, data=post_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Recommendation posted to Facebook")
            print(f"📝 {'Recommended' if recommend else 'Not recommended'}")
            return result
        else:
            # Facebook might restrict this - let's try posting to user's feed instead
            return self._post_to_feed(business_id, review_text, rating)
    
    def _post_to_feed(self, business_id: str, review_text: str, rating: int):
        """
        Fallback: Post review to user's own feed mentioning the business.
        """
        post_url = f"{self.base_url}/me/feed"
        
        # Create a post mentioning the business
        message = f"Just visited this place! {review_text} Rating: {rating}/5 ⭐"
        
        post_data = {
            'message': message,
            'place': business_id,  # Tag the business location
            'access_token': self.access_token
        }
        
        response = self.session.post(post_url, data=post_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Review posted to your Facebook feed")
            print(f"📝 Post ID: {result.get('id')}")
            return result
        else:
            raise ValueError(f"Facebook posting failed: {response.text}")

    def get_page_info(self, page_id: str) -> Dict[str, Any]:
        """
        Get information about a Facebook page.
        
        Args:
            page_id: Facebook Page ID
            
        Returns:
            Dict containing page information
        """
        if not self.access_token:
            raise ValueError("Must be logged in to get page info")
            
        page_url = f"{self.base_url}/{page_id}"
        params = {
            'access_token': self.access_token,
            'fields': 'id,name,location,phone,website,rating_count,overall_star_rating,category'
        }
        
        response = self.session.get(page_url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Failed to get page info: {response.text}")