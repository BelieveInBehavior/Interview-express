from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.core.database import get_db
from app.schemas.user import UserLogin, DirectLogin, Token, User
from app.services.user_service import user_service
from app.services.sms_service import sms_service

router = APIRouter()


# @router.post("/send-code")
# async def send_sms_code(phone: str) -> Dict[str, Any]:
#     """
#     发送短信验证码
#     
#     Args:
#         phone: 手机号码
#         
#     Returns:
#         Dict: 发送结果
#     """
#     # 验证手机号格式
#     if not phone.isdigit() or len(phone) != 11:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="手机号格式不正确"
#         )
#     
#     # 检查发送频率限制
#     if not sms_service.check_send_frequency(phone, limit_minutes=1):
#         raise HTTPException(
#             status_code=status.HTTP_429_TOO_MANY_REQUESTS,
#             detail="发送过于频繁，请稍后再试"
#         )
#     
#     # 发送验证码
#     result = sms_service.send_code(phone)
#     
#     if not result.get("success", False):
#         error_msg = result.get("message", "发送失败")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"短信发送失败: {error_msg}"
#         )
#     
#     return {
#         "message": "验证码发送成功",
#         "success": True,
#         "request_id": result.get("request_id", ""),
#         "biz_id": result.get("biz_id", "")
#     }


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录（支持验证码登录和直接登录）
    
    Args:
        user_login: 用户登录信息
        db: 数据库会话
        
    Returns:
        Token: 访问令牌
    """
    # 验证手机号格式
    if not user_login.phone.isdigit() or len(user_login.phone) != 11:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号格式不正确"
        )
    
    # 验证用户名
    if not user_login.username or len(user_login.username.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名不能为空"
        )
    
    if len(user_login.username) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名长度不能超过50个字符"
        )
    
    # 如果有验证码，进行验证码验证
    if user_login.code:
        # 验证验证码
        if not sms_service.verify_code(user_login.phone, user_login.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误或已过期"
            )
    
    try:
        # 获取或创建用户
        user = user_service.get_or_create_user(db, user_login.phone, user_login.username)
        
        # 创建访问令牌
        access_token = user_service.create_access_token_for_user(user)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/direct-login", response_model=Token)
async def direct_login(direct_login: DirectLogin, db: Session = Depends(get_db)):
    """
    直接登录（无需验证码）
    
    Args:
        direct_login: 直接登录信息
        db: 数据库会话
        
    Returns:
        Token: 访问令牌
    """
    # 验证手机号格式
    if not direct_login.phone.isdigit() or len(direct_login.phone) != 11:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号格式不正确"
        )
    try:
        # 获取或创建用户
        user = user_service.get_or_create_user(db, direct_login.phone)
        
        # 创建访问令牌
        access_token = user_service.create_access_token_for_user(user)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# @router.get("/send-status/{phone}")
# async def get_send_status(phone: str) -> Dict[str, Any]:
#     """
#     获取发送状态
#     
#     Args:
#         phone: 手机号码
#         
#     Returns:
#         Dict: 发送状态信息
#     """
#     if not phone.isdigit() or len(phone) != 11:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="手机号格式不正确"
#         )
#     
#     status_info = sms_service.get_send_status(phone)
#     return {
#         "phone": phone,
#         "has_code": status_info["has_code"],
#         "has_frequency_limit": status_info["has_frequency_limit"],
#         "code_ttl": status_info["code_ttl"],
#         "frequency_ttl": status_info["frequency_ttl"]
#     }


# @router.get("/test-code/{phone}")
# async def get_test_code(phone: str) -> Dict[str, Any]:
#     """
#     获取测试验证码（仅用于开发环境）
#     
#     Args:
#         phone: 手机号码
#         
#     Returns:
#         Dict: 测试验证码
#     """
#     if not phone.isdigit() or len(phone) != 11:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="手机号格式不正确"
#         )
#     
#     code = sms_service.get_code(phone)
#     return {
#         "phone": phone, 
#         "code": code,
#         "has_code": bool(code)
#     } 