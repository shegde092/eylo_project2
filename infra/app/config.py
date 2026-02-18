from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration from environment variables"""
    
    # API Keys
    apify_api_token: str
    openai_api_key: str

    
    # Database
    database_url: str
    
    # Queue
    redis_url: str
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    jwt_secret: str
    
    # Worker Settings
    worker_concurrency: int = 4
    retry_attempts: int = 3
    retry_delay_seconds: int = 5
    
    # Test Mode
    test_mode: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()
