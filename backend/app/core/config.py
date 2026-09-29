from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SecureDevOpsHub"
    app_env: str = "development"
    app_debug: bool = True
    app_port: int = 8000
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/securedevopshub"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    backend_cors_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
