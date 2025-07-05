from app.core.celery_app import celery_app
from app.services.sms_service import sms_service
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def send_sms_code_task(self, phone: str):
    """异步发送短信验证码任务"""
    try:
        success = sms_service.send_code(phone)
        if not success:
            raise Exception("Failed to send SMS code")
        
        logger.info(f"SMS code sent successfully to {phone}")
        return {"status": "success", "phone": phone}
    
    except Exception as exc:
        logger.error(f"Failed to send SMS code to {phone}: {exc}")
        
        # 重试机制
        if self.request.retries < self.max_retries:
            countdown = 2 ** self.request.retries  # 指数退避
            raise self.retry(exc=exc, countdown=countdown)
        
        return {"status": "failed", "phone": phone, "error": str(exc)}


@celery_app.task
def cleanup_expired_codes():
    """清理过期的验证码（可选任务）"""
    try:
        # Redis 会自动清理过期的键，这里可以添加额外的清理逻辑
        logger.info("Cleanup expired SMS codes completed")
        return {"status": "success"}
    except Exception as exc:
        logger.error(f"Cleanup failed: {exc}")
        return {"status": "failed", "error": str(exc)} 