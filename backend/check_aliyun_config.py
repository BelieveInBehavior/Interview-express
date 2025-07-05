#!/usr/bin/env python3
"""
阿里云短信服务配置检查脚本
检查阿里云短信服务的配置是否正确，并测试连接
"""

import os
import sys
import json
from typing import Dict, Any

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.config import settings
    from app.services.aliyun_sms_service import aliyun_sms_service
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保已安装所有依赖: pip install -r requirements.txt")
    sys.exit(1)


def check_aliyun_config() -> Dict[str, Any]:
    """检查阿里云短信配置"""
    print("🔍 检查阿里云短信服务配置...")
    
    config_status = {
        "access_key_id": bool(settings.ALIYUN_ACCESS_KEY_ID),
        "access_key_secret": bool(settings.ALIYUN_ACCESS_KEY_SECRET),
        "sign_name": bool(settings.ALIYUN_SMS_SIGN_NAME),
        "template_code": bool(settings.ALIYUN_SMS_TEMPLATE_CODE),
        "region_id": bool(settings.ALIYUN_SMS_REGION_ID)
    }
    
    print(f"  Access Key ID: {'✅' if config_status['access_key_id'] else '❌'}")
    print(f"  Access Key Secret: {'✅' if config_status['access_key_secret'] else '❌'}")
    print(f"  短信签名: {'✅' if config_status['sign_name'] else '❌'}")
    print(f"  模板代码: {'✅' if config_status['template_code'] else '❌'}")
    print(f"  区域ID: {'✅' if config_status['region_id'] else '❌'}")
    
    all_configured = all(config_status.values())
    
    if all_configured:
        print("✅ 阿里云短信配置完整")
    else:
        print("❌ 阿里云短信配置不完整")
        print("请检查 .env 文件中的以下配置:")
        for key, configured in config_status.items():
            if not configured:
                print(f"  - {key.upper()}")
    
    return {
        "configured": all_configured,
        "details": config_status
    }


def test_aliyun_connection() -> Dict[str, Any]:
    """测试阿里云短信服务连接"""
    print("\n🔗 测试阿里云短信服务连接...")
    
    try:
        # 测试发送验证码（使用测试手机号）
        test_phone = "13800138000"  # 测试手机号
        test_code = "123456"
        
        print(f"  测试手机号: {test_phone}")
        print(f"  测试验证码: {test_code}")
        
        result = aliyun_sms_service.send_verification_code(test_phone, test_code)
        
        if result.get("success"):
            print("✅ 阿里云短信服务连接成功")
            print(f"  请求ID: {result.get('request_id', 'N/A')}")
            print(f"  业务ID: {result.get('biz_id', 'N/A')}")
        else:
            print("❌ 阿里云短信服务连接失败")
            print(f"  错误代码: {result.get('code', 'N/A')}")
            print(f"  错误信息: {result.get('message', 'N/A')}")
        
        return result
        
    except Exception as e:
        print(f"❌ 连接测试异常: {str(e)}")
        return {
            "success": False,
            "code": "EXCEPTION",
            "message": str(e)
        }


def check_sms_service_integration() -> Dict[str, Any]:
    """检查短信服务集成"""
    print("\n🔧 检查短信服务集成...")
    
    try:
        from app.services.sms_service import sms_service
        
        if sms_service.use_aliyun:
            print("✅ 使用阿里云短信服务")
        else:
            print("⚠️  使用模拟短信服务")
            print("  原因: 阿里云配置不完整或SDK未安装")
        
        return {
            "use_aliyun": sms_service.use_aliyun,
            "available": True
        }
        
    except Exception as e:
        print(f"❌ 短信服务集成检查失败: {str(e)}")
        return {
            "use_aliyun": False,
            "available": False,
            "error": str(e)
        }


def main():
    """主函数"""
    print("=" * 60)
    print("阿里云短信服务配置检查")
    print("=" * 60)
    
    # 检查配置
    config_result = check_aliyun_config()
    
    # 检查集成
    integration_result = check_sms_service_integration()
    
    # 如果配置完整，测试连接
    if config_result["configured"]:
        connection_result = test_aliyun_connection()
    else:
        connection_result = {"success": False, "message": "配置不完整，跳过连接测试"}
    
    # 总结
    print("\n" + "=" * 60)
    print("检查总结")
    print("=" * 60)
    
    if config_result["configured"] and connection_result.get("success"):
        print("✅ 阿里云短信服务配置正确，可以正常使用")
        print("\n📝 使用说明:")
        print("1. 确保 .env 文件中的阿里云配置正确")
        print("2. 在阿里云控制台创建短信签名和模板")
        print("3. 模板参数应包含 'code' 变量")
        print("4. 测试发送验证码功能")
    elif config_result["configured"] and not connection_result.get("success"):
        print("⚠️  阿里云配置完整但连接失败")
        print("请检查:")
        print("1. Access Key 权限是否正确")
        print("2. 短信签名是否已审核通过")
        print("3. 短信模板是否已审核通过")
        print("4. 网络连接是否正常")
    else:
        print("❌ 阿里云配置不完整，将使用模拟模式")
        print("\n📝 配置说明:")
        print("1. 在阿里云控制台获取 Access Key")
        print("2. 创建短信签名并等待审核通过")
        print("3. 创建短信模板并等待审核通过")
        print("4. 更新 .env 文件中的配置")
        print("5. 重新运行此检查脚本")
    
    print("\n🔗 相关链接:")
    print("- 阿里云短信服务控制台: https://dysms.console.aliyun.com/")
    print("- 短信签名管理: https://dysms.console.aliyun.com/dysms.htm#/domestic/text/sign")
    print("- 短信模板管理: https://dysms.console.aliyun.com/dysms.htm#/domestic/text/template")
    
    return config_result["configured"] and connection_result.get("success", False)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 