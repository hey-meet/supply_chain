from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the language model.

        Args:
            prompt: Input prompt.

        Returns:
            Model response as plain text.
        """
        raise NotImplementedError