from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pydantic import BaseModel

class ReviewInput(BaseModel):
    business_name: str
    experience_text: str
    rating: Optional[int] = None
    visit_date: Optional[str] = None

class ReviewAgent:
    def __init__(self, api_key: str):
        """Initialize the review agent with OpenAI API key."""
        self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")
        self.review_template = """
        Based on the following customer experience, generate a detailed, authentic review.
        Make sure to highlight specific details and maintain a natural tone.

        Business: {business_name}
        Experience: {experience_text}
        Rating: {rating}
        Visit Date: {visit_date}

        Generate a review that captures the experience while being honest and helpful to other customers.
        Keep the review between 50-200 words and write in first person.
        """
        self.review_prompt = PromptTemplate(
            input_variables=["business_name", "experience_text", "rating", "visit_date"],
            template=self.review_template
        )
        self.review_chain = LLMChain(llm=self.llm, prompt=self.review_prompt)

    def process_voice_input(self, audio_file: str) -> str:
        """
        Process voice input and convert to text.
        To be implemented with speech recognition.
        """
        raise NotImplementedError("Voice processing to be implemented")

    def generate_review(self, review_input: ReviewInput) -> str:
        """Generate a review based on the input experience."""
        try:
            review = self.review_chain.run(**review_input.dict())
            return review.strip()
        except Exception as e:
            # Fallback if LangChain fails
            return f"Had a great experience at {review_input.business_name}. {review_input.experience_text} Would rate it {review_input.rating}/5 stars."

    def post_review(self, platform: str, review: str, **kwargs):
        """
        Post the review to the specified platform.
        To be implemented for each platform.
        """
        raise NotImplementedError(f"Posting to {platform} not yet implemented")