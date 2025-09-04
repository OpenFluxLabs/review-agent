import requests
import json
from typing import Dict, Any
from .base import ReviewPlatform

class TrustpilotPlatform(ReviewPlatform):
    def __init__(self):
        self.base_url = "https://api.trustpilot.com/v1"
        self.access_token = None
        self.session = requests.Session()

    def login(self, credentials: Dict[str, str]):
        """
        Authenticate with Trustpilot API using API key.
        
        Args:
            credentials: Dict containing 'api_key' and 'secret'
        """
        auth_url = f"{self.base_url}/oauth/oauth-business-users-for-applications/accesstoken"
        
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': credentials['api_key'],
            'client_secret': credentials['secret']
        }
        
        response = self.session.post(auth_url, data=auth_data)
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            })
            return True
        else:
            raise ValueError(f"Authentication failed: {response.text}")

    def search_business(self, business_name: str, location: str = None) -> str:
        """
        Search for a business on Trustpilot.
        
        Args:
            business_name: Name of the business
            location: Optional location filter
            
        Returns:
            str: Business domain/identifier
        """
        search_url = f"{self.base_url}/business-units/search"
        params = {
            'query': business_name,
            'country': 'US'  # Default to US, make configurable later
        }
        
        if location:
            params['location'] = location
            
        response = self.session.get(search_url, params=params)
        
        if response.status_code == 200:
            results = response.json()
            if results.get('businessUnits'):
                # Return the first match's identifier
                return results['businessUnits'][0]['identifyingName']
            else:
                raise ValueError(f"No business found for: {business_name}")
        else:
            raise ValueError(f"Search failed: {response.text}")

    def post_review(self, business_id: str, review_text: str, rating: int):
        """
        Post a review to Trustpilot.
        
        Note: Trustpilot requires invitation-based reviews for most businesses.
        This method shows the structure but may require additional setup.
        
        Args:
            business_id: Business identifier
            review_text: Review content
            rating: Rating 1-5
        """
        # Trustpilot typically requires invitation-based reviews
        # This is a simplified example - actual implementation would need
        # to handle their invitation system
        
        review_url = f"{self.base_url}/private/business-units/{business_id}/reviews"
        
        review_data = {
            'reviewText': review_text,
            'stars': rating,
            'consumer': {
                'email': 'reviewer@example.com',  # This would need to be dynamic
                'name': 'Anonymous Reviewer'
            }
        }
        
        response = self.session.post(review_url, json=review_data)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise ValueError(f"Review posting failed: {response.text}")

    def invite_review(self, business_id: str, customer_email: str, 
                     customer_name: str, reference_id: str = None):
        """
        Send a review invitation (Trustpilot's preferred method).
        
        Args:
            business_id: Business identifier
            customer_email: Customer's email
            customer_name: Customer's name
            reference_id: Optional reference ID for the transaction
        """
        invite_url = f"{self.base_url}/private/business-units/{business_id}/email-invitations"
        
        invite_data = {
            'recipient': {
                'email': customer_email,
                'name': customer_name
            },
            'referenceId': reference_id or f"review_{business_id}_{customer_email}",
            'locale': 'en-US'
        }
        
        response = self.session.post(invite_url, json=invite_data)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise ValueError(f"Invitation failed: {response.text}")