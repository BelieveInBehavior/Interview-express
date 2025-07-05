from app.models.user import User
from app.models.experience import Experience
from sqlalchemy.orm import relationship

# 添加反向关系
User.experiences = relationship("Experience", back_populates="user") 