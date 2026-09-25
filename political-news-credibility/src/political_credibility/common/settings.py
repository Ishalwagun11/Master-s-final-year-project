from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    database_url: str = "postgresql+psycopg://credibility:credibility@localhost:5432/credibility"
    async_database_url: str = (
        "postgresql+asyncpg://credibility:credibility@localhost:5432/credibility"
    )
    source_config: str = "configs/sources.yaml"
    pipeline_config: str = "configs/pipeline.yaml"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()

