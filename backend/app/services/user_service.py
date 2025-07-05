from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import create_access_token
from typing import Optional


class UserService:
    def get_user_by_phone(self, db: Session, phone: str) -> Optional[User]:
        """根据手机号获取用户"""
        return db.query(User).filter(User.phone == phone).first()
    
    def create_user(self, db: Session, user: UserCreate) -> User:
        """创建用户"""
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def update_user(self, db: Session, phone: str, user_update: UserUpdate) -> Optional[User]:
        """更新用户信息"""
        db_user = self.get_user_by_phone(db, phone)
        if not db_user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def get_or_create_user(self, db: Session, phone: str) -> User:
        """获取或创建用户"""
        user = self.get_user_by_phone(db, phone)
        if not user:
            user_data = UserCreate(phone=phone)
            user = self.create_user(db, user_data)
        return user
    
    def create_access_token_for_user(self, user: User) -> str:
        """为用户创建访问令牌"""
        return create_access_token(data={"sub": user.phone})


user_service = UserService() 