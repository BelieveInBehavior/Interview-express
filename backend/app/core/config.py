from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional
import os


class Settings(BaseSettings):
    # Database Configuration
    DATABASE_HOST: str = Field("localhost", env="DATABASE_HOST")
    DATABASE_PORT: int = Field(3306, env="DATABASE_PORT")
    DATABASE_USER: str = Field("root", env="DATABASE_USER")
    DATABASE_PASSWORD: str = Field("password", env="DATABASE_PASSWORD")
    DATABASE_NAME: str = Field("interview_express", env="DATABASE_NAME")
    DATABASE_TEST_NAME: str = Field("interview_express_test", env="DATABASE_TEST_NAME")
    DATABASE_URL_DIRECT: Optional[str] = Field(None, env="DATABASE_URL_DIRECT")
    
    # Constructed database URLs
    @property
    def database_url(self) -> str:
        if self.DATABASE_URL_DIRECT:
            return self.DATABASE_URL_DIRECT
        return f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    @property
    def database_test_url(self) -> str:
        return f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_TEST_NAME}"
    
    # Redis Configuration
    REDIS_HOST: str = Field("localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")
    REDIS_DB: int = Field(0, env="REDIS_DB")
    REDIS_PASSWORD: Optional[str] = Field(None, env="REDIS_PASSWORD")
    REDIS_URL: Optional[str] = Field(None, env="REDIS_URL")
    
    @property
    def redis_url(self) -> str:
        if self.REDIS_URL:
            return self.REDIS_URL
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # JWT Configuration
    SECRET_KEY: str = Field("your-secret-key", env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # 阿里云短信服务配置
    ALIYUN_ACCESS_KEY_ID: str = Field("", env="ALIYUN_ACCESS_KEY_ID")
    ALIYUN_ACCESS_KEY_SECRET: str = Field("", env="ALIYUN_ACCESS_KEY_SECRET")
    ALIYUN_SMS_SIGN_NAME: str = Field("", env="ALIYUN_SMS_SIGN_NAME")
    ALIYUN_SMS_TEMPLATE_CODE: str = Field("", env="ALIYUN_SMS_TEMPLATE_CODE")
    ALIYUN_SMS_REGION_ID: str = Field("cn-hangzhou", env="ALIYUN_SMS_REGION_ID")
    
    # SMS Service Configuration (保留兼容性)
    SMS_API_KEY: str = Field("mock-sms-api-key", env="SMS_API_KEY")
    SMS_SECRET: str = Field("mock-sms-secret", env="SMS_SECRET")
    
    # Server Configuration
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")
    DEBUG: bool = Field(True, env="DEBUG")
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = Field(["http://localhost:3000", "http://localhost:8081"], env="ALLOWED_ORIGINS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_prefix = ""  # No prefix for environment variables


settings = Settings() 