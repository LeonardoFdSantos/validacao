from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    default_llm_provider: str = "openai"
    default_model: str = "gpt-4o"
    redis_url: str = "redis://redis:6379/0"
    database_url: str = "postgresql://validacao:password@postgres:5432/validacao"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
