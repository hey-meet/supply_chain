from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # ------------------------------------------------------------------
    # Search Services
    # ------------------------------------------------------------------

    TAVILY_API_KEY: str

    # ------------------------------------------------------------------
    # LLM Provider Selection
    # ------------------------------------------------------------------

    LLM_PROVIDER: str = "mistral"

    # ------------------------------------------------------------------
    # Mistral Configuration
    # ------------------------------------------------------------------

    MISTRAL_API_KEY: str | None = None
    MISTRAL_MODEL: str = "mistral-small-latest"

    # ------------------------------------------------------------------
    # Gemini Configuration
    # ------------------------------------------------------------------

    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # ------------------------------------------------------------------
    # Shared LLM Settings
    # ------------------------------------------------------------------

    LLM_TEMPERATURE: float = 0.2
    LLM_TIMEOUT: int = 30

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()


settings = get_settings()