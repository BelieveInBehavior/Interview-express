import json
import logging
from typing import Dict, Any, Optional
from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from app.core.config import settings

logger = logging.getLogger(__name__)


class AliyunSMSService:
    def __init__(self):
        """初始化阿里云短信服务客户端"""
        self.client = self._create_client()
        self.sign_name = settings.ALIYUN_SMS_SIGN_NAME
        self.template_code = settings.ALIYUN_SMS_TEMPLATE_CODE
        self.region_id = settings.ALIYUN_SMS_REGION_ID
    
    def _create_client(self) -> Client:
        """创建阿里云短信客户端"""
        config = open_api_models.Config(
            access_key_id=settings.ALIYUN_ACCESS_KEY_ID,
            access_key_secret=settings.ALIYUN_ACCESS_KEY_SECRET,
            region_id=settings.ALIYUN_SMS_REGION_ID
        )
        return Client(config)
    
    def send_sms(self, phone: str, template_param: Dict[str, Any]) -> Dict[str, Any]:
        """
        发送短信
        
        Args:
            phone: 手机号码
            template_param: 模板参数
            
        Returns:
            Dict: 包含发送结果的字典
        """
        try:
            # 创建发送短信请求
            send_sms_request = dysmsapi_models.SendSmsRequest(
                phone_numbers=phone,
                sign_name=self.sign_name,
                template_code=self.template_code,
                template_param=json.dumps(template_param, ensure_ascii=False)
            )
            
            # 设置运行时选项
            runtime = util_models.RuntimeOptions()
            
            # 发送短信
            response = self.client.send_sms_with_options(send_sms_request, runtime)
            
            # 解析响应
            result = {
                "success": response.body.code == "OK",
                "code": response.body.code,
                "message": response.body.message,
                "request_id": response.body.request_id,
                "biz_id": response.body.biz_id
            }
            
            if result["success"]:
                logger.info(f"短信发送成功: {phone}, biz_id: {result['biz_id']}")
            else:
                logger.error(f"短信发送失败: {phone}, code: {result['code']}, message: {result['message']}")
            
            return result
            
        except Exception as e:
            logger.error(f"发送短信异常: {phone}, error: {str(e)}")
            return {
                "success": False,
                "code": "EXCEPTION",
                "message": str(e),
                "request_id": "",
                "biz_id": ""
            }
    
    def send_verification_code(self, phone: str, code: str) -> Dict[str, Any]:
        """
        发送验证码短信
        
        Args:
            phone: 手机号码
            code: 验证码
            
        Returns:
            Dict: 发送结果
        """
        template_param = {
            "code": code
        }
        return self.send_sms(phone, template_param)
    
    def query_send_details(self, phone: str, send_date: str, page_size: int = 10, current_page: int = 1) -> Dict[str, Any]:
        """
        查询短信发送详情
        
        Args:
            phone: 手机号码
            send_date: 发送日期 (YYYYMMDD)
            page_size: 每页记录数
            current_page: 当前页码
            
        Returns:
            Dict: 查询结果
        """
        try:
            request = dysmsapi_models.QuerySendDetailsRequest(
                phone_number=phone,
                send_date=send_date,
                page_size=page_size,
                current_page=current_page
            )
            
            runtime = util_models.RuntimeOptions()
            response = self.client.query_send_details_with_options(request, runtime)
            
            return {
                "success": response.body.code == "OK",
                "code": response.body.code,
                "message": response.body.message,
                "total_count": response.body.total_count,
                "sms_send_detail_dtos": response.body.sms_send_detail_dtos
            }
            
        except Exception as e:
            logger.error(f"查询短信详情异常: {phone}, error: {str(e)}")
            return {
                "success": False,
                "code": "EXCEPTION",
                "message": str(e),
                "total_count": 0,
                "sms_send_detail_dtos": []
            }


# 创建全局实例
aliyun_sms_service = AliyunSMSService() 