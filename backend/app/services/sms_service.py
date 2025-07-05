import redis
import json
from app.core.config import settings
from app.core.security import generate_sms_code


class SMSService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.redis_url)
        self.code_expire = 300  # 验证码5分钟过期
    
    def send_code(self, phone: str) -> bool:
        """发送验证码"""
        try:
            # 生成验证码
            code = generate_sms_code()
            
            # 存储到Redis，5分钟过期
            key = f"sms_code:{phone}"
            self.redis_client.setex(key, self.code_expire, code)
            
            # 这里应该调用真实的短信API
            # 目前只是模拟发送
            print(f"发送验证码到 {phone}: {code}")
            
            return True
        except Exception as e:
            print(f"发送验证码失败: {e}")
            return False
    
    def verify_code(self, phone: str, code: str) -> bool:
        """验证验证码"""
        try:
            key = f"sms_code:{phone}"
            stored_code = self.redis_client.get(key)
            
            if stored_code and stored_code.decode() == code:
                # 验证成功后删除验证码
                self.redis_client.delete(key)
                return True
            return False
        except Exception as e:
            print(f"验证码验证失败: {e}")
            return False
    
    def get_code(self, phone: str) -> str:
        """获取验证码（仅用于测试）"""
        try:
            key = f"sms_code:{phone}"
            code = self.redis_client.get(key)
            return code.decode() if code else ""
        except Exception:
            return ""


sms_service = SMSService() 