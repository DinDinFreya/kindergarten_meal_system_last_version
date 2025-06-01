# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # ==== Database ====
    DATABASE_URL: str

    # ==== Redis & Celery ====
    REDIS_URL: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # ==== API Info ====
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Kindergarten Meal Tracking System"

    # ==== JWT Auth ====
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ==== Business Logic Thresholds ====
    LOW_STOCK_THRESHOLD: int = 500  # grams
    DISCREPANCY_THRESHOLD: float = 15.0  # percentage

    # ==== Environment File Configuration ====
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()
