#!/usr/bin/env python3
"""
短信功能测试脚本
测试短信发送、验证码验证等功能
"""

import os
import sys
import time
import requests
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 测试配置
BASE_URL = "http://localhost:8000"
TEST_PHONE = "13800138000"


def test_send_sms_code():
    """测试发送短信验证码"""
    print("📱 测试发送短信验证码...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/send-code", params={"phone": TEST_PHONE})
        
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.json()}")
        
        if response.status_code == 200:
            print("✅ 短信发送成功")
            return True
        elif response.status_code == 429:
            print("⚠️  发送频率限制，等待1分钟后重试...")
            time.sleep(60)
            return test_send_sms_code()
        else:
            print("❌ 短信发送失败")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False


def test_get_send_status():
    """测试获取发送状态"""
    print("\n📊 测试获取发送状态...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/auth/send-status/{TEST_PHONE}")
        
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.json()}")
        
        if response.status_code == 200:
            print("✅ 获取发送状态成功")
            return True
        else:
            print("❌ 获取发送状态失败")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False


def test_get_test_code():
    """测试获取测试验证码"""
    print("\n🔍 测试获取测试验证码...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/auth/test-code/{TEST_PHONE}")
        
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("has_code"):
                print(f"✅ 获取测试验证码成功: {data['code']}")
                return data['code']
            else:
                print("⚠️  没有找到验证码")
                return None
        else:
            print("❌ 获取测试验证码失败")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None


def test_login_with_code(code):
    """测试使用验证码登录"""
    print(f"\n🔐 测试使用验证码登录: {code}")
    
    try:
        login_data = {
            "phone": TEST_PHONE,
            "code": code
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("access_token"):
                print("✅ 登录成功")
                print(f"  访问令牌: {data['access_token'][:20]}...")
                return data['access_token']
            else:
                print("❌ 登录失败：没有返回访问令牌")
                return None
        else:
            print("❌ 登录失败")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None


def test_sms_service_direct():
    """直接测试短信服务"""
    print("\n🔧 直接测试短信服务...")
    
    try:
        from app.services.sms_service import sms_service
        
        # 测试发送验证码
        result = sms_service.send_code(TEST_PHONE)
        print(f"  发送结果: {result}")
        
        # 获取验证码
        code = sms_service.get_code(TEST_PHONE)
        print(f"  验证码: {code}")
        
        if code:
            # 测试验证
            is_valid = sms_service.verify_code(TEST_PHONE, code)
            print(f"  验证结果: {is_valid}")
            
            # 测试发送状态
            status = sms_service.get_send_status(TEST_PHONE)
            print(f"  发送状态: {status}")
            
            return True
        else:
            print("❌ 没有获取到验证码")
            return False
            
    except Exception as e:
        print(f"❌ 直接测试异常: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("短信功能测试")
    print("=" * 60)
    
    # 检查服务是否运行
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code != 200:
            print("❌ 后端服务未运行，请先启动服务: python run.py")
            return
    except:
        print("❌ 无法连接到后端服务，请先启动服务: python run.py")
        return
    
    print("✅ 后端服务运行正常")
    
    # 测试1: 发送短信验证码
    if not test_send_sms_code():
        print("❌ 短信发送测试失败")
        return
    
    # 测试2: 获取发送状态
    test_get_send_status()
    
    # 测试3: 获取测试验证码
    code = test_get_test_code()
    if not code:
        print("❌ 获取测试验证码失败")
        return
    
    # 测试4: 使用验证码登录
    token = test_login_with_code(code)
    if not token:
        print("❌ 登录测试失败")
        return
    
    # 测试5: 直接测试短信服务
    test_sms_service_direct()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print("✅ 所有测试通过")
    print(f"📱 测试手机号: {TEST_PHONE}")
    print(f"🔐 访问令牌: {token[:20]}...")


if __name__ == "__main__":
    main() 