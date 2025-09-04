from abc import ABC, abstractmethod
from typing import Dict, Any

class ReviewPlatform(ABC):
    @abstractmethod
    def login(self, credentials: Dict[str, str]):
        """Login to the platform"""
        pass

    @abstractmethod
    def post_review(self, business_id: str, review_text: str, rating: int):
        """Post a review for the specified business"""
        pass

    @abstractmethod
    def search_business(self, business_name: str, location: str) -> str:
        """Search for a business and return its ID"""
        pass