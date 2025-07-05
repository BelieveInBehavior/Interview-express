import redis
import json
import logging
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.security import generate_sms_code

# 尝试导入阿里云短信服务
try:
    from .aliyun_sms_service import aliyun_sms_service
    ALIYUN_AVAILABLE = True
except ImportError:
    ALIYUN_AVAILABLE = False
    logging.warning("阿里云短信SDK未安装，将使用模拟模式")

logger = logging.getLogger(__name__)


class SMSService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.redis_url)
        self.code_expire = 300  # 验证码5分钟过期
        self.use_aliyun = ALIYUN_AVAILABLE and self._check_aliyun_config()
        
        if self.use_aliyun:
            logger.info("使用阿里云短信服务")
        else:
            logger.info("使用模拟短信服务")
    
    def _check_aliyun_config(self) -> bool:
        """检查阿里云配置是否完整"""
        required_fields = [
            settings.ALIYUN_ACCESS_KEY_ID,
            settings.ALIYUN_ACCESS_KEY_SECRET,
            settings.ALIYUN_SMS_SIGN_NAME,
            settings.ALIYUN_SMS_TEMPLATE_CODE
        ]
        return all(field for field in required_fields)
    
    def send_code(self, phone: str) -> Dict[str, Any]:
        """
        发送验证码
        
        Args:
            phone: 手机号码
            
        Returns:
            Dict: 包含发送结果的字典
        """
        try:
            # 生成验证码
            code = generate_sms_code()
            
            # 存储到Redis，5分钟过期
            key = f"sms_code:{phone}"
            self.redis_client.setex(key, self.code_expire, code)
            
            # 发送短信
            if self.use_aliyun:
                result = aliyun_sms_service.send_verification_code(phone, code)
            else:
                # 模拟发送
                result = self._mock_send_sms(phone, code)
            
            return result
            
        except Exception as e:
            logger.error(f"发送验证码失败: {phone}, error: {str(e)}")
            return {
                "success": False,
                "code": "EXCEPTION",
                "message": str(e),
                "request_id": "",
                "biz_id": ""
            }
    
    def _mock_send_sms(self, phone: str, code: str) -> Dict[str, Any]:
        """模拟发送短信（用于测试）"""
        logger.info(f"模拟发送验证码到 {phone}: {code}")
        return {
            "success": True,
            "code": "OK",
            "message": "模拟发送成功",
            "request_id": f"mock_{phone}_{code}",
            "biz_id": f"mock_biz_{phone}_{code}"
        }
    
    def verify_code(self, phone: str, code: str) -> bool:
        """
        验证验证码
        
        Args:
            phone: 手机号码
            code: 验证码
            
        Returns:
            bool: 验证是否成功
        """
        try:
            key = f"sms_code:{phone}"
            stored_code = self.redis_client.get(key)
            
            if stored_code and stored_code.decode() == code:
                # 验证成功后删除验证码
                self.redis_client.delete(key)
                logger.info(f"验证码验证成功: {phone}")
                return True
            
            logger.warning(f"验证码验证失败: {phone}, 输入: {code}")
            return False
            
        except Exception as e:
            logger.error(f"验证码验证异常: {phone}, error: {str(e)}")
            return False
    
    def get_code(self, phone: str) -> str:
        """
        获取验证码（仅用于测试）
        
        Args:
            phone: 手机号码
            
        Returns:
            str: 验证码
        """
        try:
            key = f"sms_code:{phone}"
            code = self.redis_client.get(key)
            return code.decode() if code else ""
        except Exception as e:
            logger.error(f"获取验证码异常: {phone}, error: {str(e)}")
            return ""
    
    def check_send_frequency(self, phone: str, limit_minutes: int = 1) -> bool:
        """
        检查发送频率限制
        
        Args:
            phone: 手机号码
            limit_minutes: 限制时间（分钟）
            
        Returns:
            bool: 是否可以发送
        """
        try:
            key = f"sms_frequency:{phone}"
            last_send_time = self.redis_client.get(key)
            
            if last_send_time:
                # 检查是否在限制时间内
                import time
                current_time = int(time.time())
                last_time = int(last_send_time.decode())
                
                if current_time - last_time < limit_minutes * 60:
                    return False
            
            # 记录发送时间
            self.redis_client.setex(key, limit_minutes * 60, str(int(time.time())))
            return True
            
        except Exception as e:
            logger.error(f"检查发送频率异常: {phone}, error: {str(e)}")
            return True  # 异常时允许发送
    
    def get_send_status(self, phone: str) -> Dict[str, Any]:
        """
        获取发送状态
        
        Args:
            phone: 手机号码
            
        Returns:
            Dict: 发送状态信息
        """
        try:
            code_key = f"sms_code:{phone}"
            frequency_key = f"sms_frequency:{phone}"
            
            code_exists = self.redis_client.exists(code_key)
            frequency_exists = self.redis_client.exists(frequency_key)
            
            return {
                "has_code": bool(code_exists),
                "has_frequency_limit": bool(frequency_exists),
                "code_ttl": self.redis_client.ttl(code_key) if code_exists else 0,
                "frequency_ttl": self.redis_client.ttl(frequency_key) if frequency_exists else 0
            }
            
        except Exception as e:
            logger.error(f"获取发送状态异常: {phone}, error: {str(e)}")
            return {
                "has_code": False,
                "has_frequency_limit": False,
                "code_ttl": 0,
                "frequency_ttl": 0
            }


# 创建全局实例
sms_service = SMSService() 