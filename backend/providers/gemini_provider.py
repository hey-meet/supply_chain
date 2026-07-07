from google import genai

from backend.config.settings import settings
from backend.providers.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    """Google Gemini provider."""

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def generate(self, prompt: str) -> str:
        """Generate a response using Gemini."""

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )

        return response.text