from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    embedding_dimensions: int = 1536
    database_url: str
    jwt_secret: str
    model_api_key: str = "LOCAL_ONLY_NO_PROVIDER_KEY_CONFIGURED"
    model_name: str = "LOCAL_ONLY_SELECT_A_PROVIDER_MODEL"
    embedding_model: str = "LOCAL_ONLY_SELECT_A_PROVIDER_EMBEDDING_MODEL"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
