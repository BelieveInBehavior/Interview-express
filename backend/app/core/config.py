from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Database
    database_url: str = "mysql+pymysql://root:password@localhost:3306/interview_express"
    database_test_url: str = "mysql+pymysql://root:password@localhost:3306/interview_express_test"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # SMS Service
    sms_api_key: str = "mock-sms-api-key"
    sms_secret: str = "mock-sms-secret"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8081"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings() 