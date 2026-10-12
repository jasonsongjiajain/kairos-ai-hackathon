from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Storage has separate, fixed-size columns for these supported dimensions.
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
    customer_chat_provider: Literal["local", "hosted"] = "local"
    customer_chat_mode: Literal["guided", "agent"] = "guided"
    customer_agent_max_steps: int = Field(default=6, ge=3, le=10)
    customer_router_simulation_enabled: bool = False
    app_environment: Literal["development", "test", "production"] = "production"
    model_tls_verify: bool = True
    diagnostic_max_age_seconds: int = 900

    @model_validator(mode="after")
    def require_development_for_insecure_model_tls(self) -> "Settings":
        if self.customer_router_simulation_enabled and self.app_environment == "production":
            raise ValueError("Router simulation is limited to development and test environments")
        if not self.model_tls_verify and self.app_environment != "development":
            raise ValueError("MODEL_TLS_VERIFY=false requires APP_ENVIRONMENT=development")
        return self

    @field_validator("diagnostic_max_age_seconds")
    @classmethod
    def require_positive_diagnostic_max_age(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Diagnostic freshness must be a positive number of seconds")
        return value

    @field_validator("embedding_dimensions")
    @classmethod
    def require_supported_embedding_dimensions(cls, value: int) -> int:
        if value not in (1024, 1536):
            raise ValueError("Supported embedding dimensions are 1024 and 1536; other sizes require a new migration")
        return value

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
