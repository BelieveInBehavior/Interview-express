#!/usr/bin/env python3
"""
测试直接登录功能
"""
import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000/api/v1"

def test_direct_login():
    """测试直接登录"""
    print("🧪 测试直接登录功能")
    print("=" * 50)
    
    # 测试数据
    test_cases = [
        {
            "name": "正常登录",
            "data": {
                "phone": "13800138000",
                "username": "testuser1"
            }
        },
        {
            "name": "用户名已存在",
            "data": {
                "phone": "13800138001",
                "username": "testuser1"  # 使用相同的用户名
            }
        },
        {
            "name": "手机号已存在，更新用户名",
            "data": {
                "phone": "13800138000",  # 使用相同的手机号
                "username": "testuser2"  # 不同的用户名
            }
        },
        {
            "name": "无效手机号",
            "data": {
                "phone": "12345678901",
                "username": "testuser3"
            }
        },
        {
            "name": "空用户名",
            "data": {
                "phone": "13800138002",
                "username": ""
            }
        },
        {
            "name": "超长用户名",
            "data": {
                "phone": "13800138003",
                "username": "a" * 51  # 51个字符
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   手机号: {test_case['data']['phone']}")
        print(f"   用户名: {test_case['data']['username']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/auth/direct-login",
                json=test_case['data'],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ 成功")
                print(f"   用户ID: {result['user']['id']}")
                print(f"   用户名: {result['user']['username']}")
                print(f"   手机号: {result['user']['phone']}")
                print(f"   令牌: {result['access_token'][:20]}...")
            else:
                error = response.json()
                print(f"   ❌ 失败: {error.get('detail', '未知错误')}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ 连接失败: 请确保后端服务正在运行 (python run.py)")
        except Exception as e:
            print(f"   ❌ 请求失败: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成！")

if __name__ == "__main__":
    test_direct_login() 