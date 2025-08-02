import os
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any


class Settings(BaseSettings):
    PROJECT_NAME: str = "SnapWave"
    API_V1_STR: str = "/api/v1"
    
    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://shukla@localhost:5432/snapwave"
    )
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["*"]  # In production, set specific origins

    # Storage settings
    STORAGE_ENDPOINT: str = os.getenv("STORAGE_ENDPOINT", "localhost:9000")
    STORAGE_ACCESS_KEY: str = os.getenv("STORAGE_ACCESS_KEY", "minioaccess")
    STORAGE_SECRET_KEY: str = os.getenv("STORAGE_SECRET_KEY", "miniosecret")
    STORAGE_BUCKET_NAME: str = os.getenv("STORAGE_BUCKET_NAME", "snapwave")
    STORAGE_USE_HTTPS: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
