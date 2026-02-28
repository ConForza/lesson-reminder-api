from functools import lru_cache
from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "Lesson Reminder API"
    api_v1_prefix: str = "/api/v1"
    environment: str = "local"
    version: str = "0.1.0"

@lru_cache
def get_settings() -> Settings:
    return Settings()