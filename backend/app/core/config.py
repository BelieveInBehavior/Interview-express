from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Database Configuration
    database_host: str = "localhost" 
    database_port: int = 3306
    database_user: str = "root"
    database_password: str = "password"
    database_name: str = "interview_express"
    database_test_name: str = "interview_express_test"
    
    # Constructed database URLs
    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"
    
    @property
    def database_test_url(self) -> str:
        return f"mysql+pymysql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_test_name}"
    
    # Alternative: Direct database URL (if provided)
    database_url_direct: Optional[str] = None
    
    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    
    @property
    def redis_url(self) -> str:
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    # JWT Configuration
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # SMS Service Configuration
    sms_api_key: str = "mock-sms-api-key"
    sms_secret: str = "mock-sms-secret"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # CORS Configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8081"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_prefix = ""  # No prefix for environment variables


settings = Settings() 