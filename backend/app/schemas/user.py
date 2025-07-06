from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    phone: str = Field(..., description="手机号码", min_length=11, max_length=11)
    username: str = Field(..., description="用户名", min_length=1, max_length=50)
    avatar: Optional[str] = Field(None, description="头像URL")
    bio: Optional[str] = Field(None, description="个人简介")


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    avatar: Optional[str] = None
    bio: Optional[str] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class User(UserInDB):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    phone: str = Field(..., description="手机号码", min_length=11, max_length=11)
    username: str = Field(..., description="用户名", min_length=1, max_length=50)
    code: Optional[str] = Field(None, description="短信验证码（可选）", min_length=4, max_length=6)


class DirectLogin(BaseModel):
    phone: str = Field(..., description="手机号码", min_length=11, max_length=11)
    # username: str = Field(..., description="用户名", min_length=1, max_length=50)


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User


class TokenData(BaseModel):
    phone: Optional[str] = None 