from app.core.database import Base
from app.models.user import User
from app.models.experience import Experience
from sqlalchemy.orm import relationship

# 添加反向关系
User.experiences = relationship("Experience", back_populates="user")

# 导出所有模型
__all__ = ["Base", "User", "Experience"] 