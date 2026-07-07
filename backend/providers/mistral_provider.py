from mistralai.client import Mistral

from backend.config.settings import settings
from backend.providers.base import BaseLLMProvider


class MistralProvider(BaseLLMProvider):
    """Mistral AI provider."""

    def __init__(self):
        self.client = Mistral(
            api_key=settings.MISTRAL_API_KEY,
        )

    def generate(self, prompt: str) -> str:
        """Generate a response using Mistral."""

        response = self.client.chat.complete(
            model=settings.MISTRAL_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=settings.LLM_TEMPERATURE,
        )

        return response.choices[0].message.content