"""Typed application settings, loaded once from environment variables / `.env`.

Every module reads configuration from `settings` instead of calling `config()`
so a missing or malformed variable fails at startup, not on the first request.
"""

from functools import lru_cache
from typing import Annotated, Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

CommaList = Annotated[list[str], NoDecode]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- app
    APP_NAME: str = "{{ cookiecutter.project_name }}"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: Literal["dev", "staging", "prod"] = "dev"
    LOG_LEVEL: str = "INFO"
    PORT: int = 3000
    WORKERS: int = 1

    # --- security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    FERNET_KEY: str
    # key used to build deterministic hashes of encrypted fields (email lookup)
    BLIND_INDEX_KEY: str
    ALLOW_ORIGINS: CommaList = ["http://localhost:5173", "http://localhost:4173"]
    ALLOWED_HOSTS: CommaList = ["*"]
    MAX_BODY_SIZE: int = 10 * 1024 * 1024  # bytes
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # bytes
    ALLOWED_UPLOAD_TYPES: CommaList = ["image/png", "image/jpeg", "image/webp", "application/pdf"]

    # --- rate limit / cache
    RATE_LIMIT_DEFAULT: str = "100/minute"
    RATE_LIMIT_AUTH: str = "5/minute"
    CACHE_TTL: int = 60
    REDIS_URL: str | None = None

    # --- scheduler (enable on ONE instance only when running several replicas)
    SCHEDULER_ENABLED: bool = True
{% if cookiecutter.database == 'mongodb' %}
    # --- mongodb
    MONGODB_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "{{ cookiecutter.package_slug }}"
{% elif cookiecutter.database == 'supabase' %}
    # --- supabase (use the service-role key server-side, never ship it to a frontend)
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_BUCKET_NAME: str = "uploads"
{% endif %}
    @field_validator("ALLOW_ORIGINS", "ALLOWED_HOSTS", "ALLOWED_UPLOAD_TYPES", mode="before")
    @classmethod
    def split_commas(cls, value):
        if isinstance(value, str):
            return [v.strip() for v in value.split(",") if v.strip()]
        return value

    @property
    def is_prod(self) -> bool:
        return self.ENVIRONMENT == "prod"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
