from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # ------------------------------------------------------------------
    # Application & General Settings
    # ------------------------------------------------------------------

    APP_NAME: str = "Supply Chain Intelligence"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    API_V1_STR: str = "/api/v1"

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
        env_file=(_ENV_FILE, "backend/.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()


settings = get_settings()