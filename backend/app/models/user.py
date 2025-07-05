from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    # 使用手机号作为主键
    phone = Column(String(11), primary_key=True, index=True)
    username = Column(String(50), nullable=True)
    avatar = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(phone={self.phone}, username={self.username})>" 