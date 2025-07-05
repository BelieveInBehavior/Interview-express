from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserLogin, Token, User
from app.services.user_service import user_service
from app.services.sms_service import sms_service

router = APIRouter()


@router.post("/send-code")
async def send_sms_code(phone: str):
    """发送短信验证码"""
    if not phone.isdigit() or len(phone) != 11:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number"
        )
    
    success = sms_service.send_code(phone)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send SMS code"
        )
    
    return {"message": "SMS code sent successfully"}


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    # 验证验证码
    if not sms_service.verify_code(user_login.phone, user_login.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )
    
    # 获取或创建用户
    user = user_service.get_or_create_user(db, user_login.phone)
    
    # 创建访问令牌
    access_token = user_service.create_access_token_for_user(user)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/test-code/{phone}")
async def get_test_code(phone: str):
    """获取测试验证码（仅用于开发环境）"""
    code = sms_service.get_code(phone)
    return {"phone": phone, "code": code} 