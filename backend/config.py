# backend/config.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Logistics Autonomous Disruption Monitoring Agent"
    API_V1_STR: str = "/api/v1"
    
    # Read DEBUG from env; default to False for security if not specified
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    LOG_LEVEL: str = "INFO"

    # Pydantic v2 configuration style
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()