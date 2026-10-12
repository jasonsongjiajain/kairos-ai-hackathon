from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # This initial schema is fixed at 1536. A different size needs a new migration.
    embedding_dimensions: int = 1536
    rag_minimum_score: float = 0.0
    demo_seed_enabled: bool = False
    database_url: str
    jwt_secret: str
    model_api_key: str = "LOCAL_ONLY_NO_PROVIDER_KEY_CONFIGURED"
    model_name: str = "gigx/gemma-4-e2b-it"
    reasoning_model_name: str = "gigx/qwen3-vl-4b-instruct"
    model_base_url: str = "https://gigx.nexa-dev.tm.com.my/llm/v1"
    embedding_model: str = "gigx/qwen3-embedding-0.6b"
    # Local mode remains key-free. Set both provider variables to "hosted" to use GIGX.
    embedding_provider: str = "local"
    model_provider: str = "local"
    reasoning_provider: str = "local"
    # Internal endpoints may use a private CA. Set MODEL_CA_BUNDLE to a CA file,
    # or MODEL_TLS_VERIFY=false for a trusted internal dev-only endpoint.
    model_tls_verify: bool = True
    model_ca_bundle: str | None = None

    @field_validator("embedding_dimensions")
    @classmethod
    def require_initial_embedding_dimensions(cls, value: int) -> int:
        if value != 1536:
            raise ValueError("The initial schema uses 1536 dimensions; changing it requires a new migration")
        return value

    @field_validator("rag_minimum_score")
    @classmethod
    def require_valid_rag_threshold(cls, value: float) -> float:
        if not 0.0 <= value <= 1.0:
            raise ValueError("RAG_MINIMUM_SCORE must be between 0 and 1")
        return value

    @field_validator("model_base_url")
    @classmethod
    def normalize_model_base_url(cls, value: str) -> str:
        return value.rstrip("/")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
