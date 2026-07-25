import os
import warnings
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "LinkedIn Post Generator API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000

    # Security & Auth
    SECRET_KEY: str = "dev-secret-key-please-change-in-prod"
    JWT_SECRET_KEY: str = "dev-jwt-secret-key-please-change-in-prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Database
    DATABASE_URL: str = "sqlite:///./linkedin_posts.db"

    # LLM Settings
    LLM_PROVIDER: str = "groq"
    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    MAX_LLM_TOKENS_PER_POST: int = 1000

    # CORS
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:5500,http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=(".env", "backend/.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        return ["*"]


settings = Settings()

# Validate insecure defaults in production
if settings.ENVIRONMENT.lower() == "production":
    if "dev-secret" in settings.SECRET_KEY or "dev-jwt" in settings.JWT_SECRET_KEY:
        warnings.warn("SECURITY WARNING: Using placeholder secret keys in production! Set SECRET_KEY and JWT_SECRET_KEY in environment variables.")
