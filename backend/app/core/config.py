from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    APP_NAME: str = "Nexora"
    APP_ENV: str = "development"

    LLM_PROVIDER: str = "mock"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.8-flash"

    DATABASE_URL: str = "sqlite:///./nexora.db"

    MAX_AGENT_ITERATIONS: int = 5
    MAX_TOOL_CALLS: int = 5

    # ---------------------------------------------------------
    # Educational image search
    # ---------------------------------------------------------

    GOOGLE_CSE_API_KEY: str = ""
    GOOGLE_CSE_ID: str = ""

    IMAGE_SEARCH_ENABLED: bool = True
    IMAGE_SEARCH_LIMIT: int = 4

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()