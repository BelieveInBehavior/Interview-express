#!/usr/bin/env python3
"""
直接登录功能测试脚本
测试手机号直接登录功能
"""

import os
import sys
import requests
import json

# 测试配置
BASE_URL = "http://localhost:8000"
TEST_PHONE = "13800138000"


def test_direct_login():
    """测试直接登录功能"""
    print("🔐 测试直接登录功能...")
    
    try:
        login_data = {
            "phone": TEST_PHONE
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/direct-login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("access_token"):
                print("✅ 直接登录成功")
                print(f"  访问令牌: {data['access_token'][:20]}...")
                print(f"  用户信息: {data['user']['phone']}")
                return data['access_token']
            else:
                print("❌ 直接登录失败：没有返回访问令牌")
                return None
        else:
            print("❌ 直接登录失败")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None


def test_login_without_code():
    """测试不带验证码的登录"""
    print("\n📱 测试不带验证码的登录...")
    
    try:
        login_data = {
            "phone": TEST_PHONE,
            "code": None  # 不提供验证码
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
                print("✅ 不带验证码登录成功")
                return data['access_token']
            else:
                print("❌ 不带验证码登录失败")
                return None
        else:
            print("❌ 不带验证码登录失败")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None


def test_login_with_code():
    """测试带验证码的登录"""
    print("\n📱 测试带验证码的登录...")
    
    try:
        # 先发送验证码
        send_response = requests.post(
            f"{BASE_URL}/api/v1/auth/send-code",
            params={"phone": TEST_PHONE}
        )
        
        if send_response.status_code != 200:
            print("❌ 发送验证码失败")
            return None
        
        # 获取测试验证码
        code_response = requests.get(f"{BASE_URL}/api/v1/auth/test-code/{TEST_PHONE}")
        
        if code_response.status_code != 200:
            print("❌ 获取测试验证码失败")
            return None
        
        code_data = code_response.json()
        code = code_data.get("code")
        
        if not code:
            print("❌ 没有获取到验证码")
            return None
        
        print(f"  获取到验证码: {code}")
        
        # 使用验证码登录
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
                print("✅ 带验证码登录成功")
                return data['access_token']
            else:
                print("❌ 带验证码登录失败")
                return None
        else:
            print("❌ 带验证码登录失败")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None


def test_invalid_phone():
    """测试无效手机号"""
    print("\n❌ 测试无效手机号...")
    
    try:
        login_data = {
            "phone": "12345678901"  # 无效手机号
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/direct-login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.json()}")
        
        if response.status_code == 400:
            print("✅ 无效手机号验证正确")
            return True
        else:
            print("❌ 无效手机号验证失败")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("直接登录功能测试")
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
    
    # 测试1: 直接登录
    token1 = test_direct_login()
    if not token1:
        print("❌ 直接登录测试失败")
        return
    
    # 测试2: 不带验证码登录
    token2 = test_login_without_code()
    if not token2:
        print("❌ 不带验证码登录测试失败")
        return
    
    # 测试3: 带验证码登录
    token3 = test_login_with_code()
    if not token3:
        print("❌ 带验证码登录测试失败")
        return
    
    # 测试4: 无效手机号
    invalid_test = test_invalid_phone()
    if not invalid_test:
        print("❌ 无效手机号测试失败")
        return
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print("✅ 所有测试通过")
    print(f"📱 测试手机号: {TEST_PHONE}")
    print(f"🔐 直接登录令牌: {token1[:20]}...")
    print(f"🔐 无验证码登录令牌: {token2[:20]}...")
    print(f"🔐 有验证码登录令牌: {token3[:20]}...")
    
    print("\n📝 功能说明:")
    print("1. 用户可以选择直接登录（无需验证码）")
    print("2. 用户也可以选择验证码登录")
    print("3. 两种方式都会创建或获取用户账号")
    print("4. 都会返回有效的访问令牌")


if __name__ == "__main__":
    main() 