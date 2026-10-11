from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # This initial schema is fixed at 1536. A different size needs a new migration.
    embedding_dimensions: int = 1536
    demo_seed_enabled: bool = False
    database_url: str
    jwt_secret: str
    model_api_key: str = "LOCAL_ONLY_NO_PROVIDER_KEY_CONFIGURED"
    model_name: str = "LOCAL_ONLY_SELECT_A_PROVIDER_MODEL"
    model_base_url: str = "LOCAL_ONLY_NO_PROVIDER_BASE_URL_CONFIGURED"
    embedding_model: str = "LOCAL_ONLY_SELECT_A_PROVIDER_EMBEDDING_MODEL"
    # "local" keeps the app key-free; "hosted" routes through an OpenAI-compatible API.
    embedding_provider: str = "local"
    model_provider: str = "local"

    @field_validator("embedding_dimensions")
    @classmethod
    def require_initial_embedding_dimensions(cls, value: int) -> int:
        if value != 1536:
            raise ValueError("The initial schema uses 1536 dimensions; changing it requires a new migration")
        return value

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
