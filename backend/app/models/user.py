from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    # 使用自增ID作为主键
    id = Column(Integer, primary_key=True, index=True)
    # 手机号作为唯一索引
    phone = Column(String(11), unique=True, index=True, nullable=False)
    # 用户名为必填项
    username = Column(String(50), nullable=False)
    avatar = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    experiences = relationship("Experience", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, phone={self.phone}, username={self.username})>" 