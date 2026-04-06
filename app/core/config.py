from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    api_v1_prefix: str
    environment: str
    version: str

    jwt_secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=".env"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()