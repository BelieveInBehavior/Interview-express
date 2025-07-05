from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Experience(Base):
    __tablename__ = "experiences"
    
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(100), nullable=False, index=True)
    position = Column(String(100), nullable=False, index=True)
    summary = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    difficulty = Column(Float, default=0.0)  # 难度评分 0-5
    tags = Column(Text, nullable=True)  # JSON格式存储标签
    user_phone = Column(String(11), ForeignKey("users.phone"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="experiences")
    
    def __repr__(self):
        return f"<Experience(id={self.id}, company={self.company}, position={self.position})>" 