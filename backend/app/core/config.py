import os
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any


class Settings(BaseSettings):
    PROJECT_NAME: str = "SnapWave"
    API_V1_STR: str = "/api/v1"
    EMAIL_DEV_MODE: bool = True  # Set to False in production
    
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
    
    # Email settings
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "info@snapwave.com")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "SnapWave")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "587"))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS", "True").lower() == "true"
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS", "False").lower() == "true"
    MAIL_USE_CREDENTIALS: bool = os.getenv("MAIL_USE_CREDENTIALS", "True").lower() == "true"
    MAIL_VALIDATE_CERTS: bool = os.getenv("MAIL_VALIDATE_CERTS", "True").lower() == "true"
    
    # Frontend URL for links in emails
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    STORAGE_SECRET_KEY: str = os.getenv("STORAGE_SECRET_KEY", "miniosecret")
    STORAGE_BUCKET_NAME: str = os.getenv("STORAGE_BUCKET_NAME", "snapwave")
    STORAGE_USE_HTTPS: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
