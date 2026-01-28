from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration from environment variables"""
    
    # API Keys
    apify_api_token: str
    gemini_api_key: str
    fcm_server_key: str
    
    # Database
    database_url: str
    
    # Queue
    redis_url: str
    
    # Storage
    aws_s3_bucket: str
    aws_region: str = "us-east-1"
    aws_access_key_id: str
    aws_secret_access_key: str
    
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


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()
