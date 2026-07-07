from backend.config.settings import settings
from backend.providers.gemini_provider import GeminiProvider
from backend.providers.mistral_provider import MistralProvider


class LLMClient:
    """Factory for interacting with the configured LLM provider."""

    def __init__(self):
        provider = settings.LLM_PROVIDER.lower()

        if provider == "mistral":
            self.provider = MistralProvider()

        elif provider == "gemini":
            self.provider = GeminiProvider()

        else:
            raise ValueError(
                f"Unsupported LLM provider: {provider}"
            )

    def generate(self, prompt: str) -> str:
        """
        Generate a response using the configured provider.

        Raises:
            RuntimeError: If the provider request fails.
        """

        try:
            return self.provider.generate(prompt)

        except Exception as exc:
            raise RuntimeError(
                f"LLM generation failed: {exc}"
            ) from exc