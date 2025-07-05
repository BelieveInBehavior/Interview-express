#!/usr/bin/env python3
"""
配置检查脚本
用于验证环境变量和数据库连接配置
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from app.core.config import settings
    import pymysql
    import redis
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保已安装所有依赖: pip install -r requirements.txt")
    sys.exit(1)


def check_env_file():
    """检查环境变量文件"""
    env_file = project_root / ".env"
    if not env_file.exists():
        print("⚠️  .env 文件不存在")
        print("   请复制 env.example 为 .env 并配置相关参数")
        return False
    
    print("✅ .env 文件存在")
    return True


def check_database_config():
    """检查数据库配置"""
    print("\n📊 数据库配置:")
    print(f"   主机: {settings.database_host}")
    print(f"   端口: {settings.database_port}")
    print(f"   用户: {settings.database_user}")
    print(f"   数据库: {settings.database_name}")
    print(f"   测试数据库: {settings.database_test_name}")
    
    if settings.database_url_direct:
        print(f"   直接URL: {settings.database_url_direct}")
    else:
        print(f"   构建URL: {settings.database_url}")


def test_database_connection():
    """测试数据库连接"""
    print("\n🔍 测试数据库连接...")
    try:
        conn = pymysql.connect(
            host=settings.database_host,
            user=settings.database_user,
            password=settings.database_password,
            database=settings.database_name,
            port=settings.database_port
        )
        print("✅ 数据库连接成功")
        
        # 检查数据库是否存在
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"   现有表数量: {len(tables)}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False


def check_redis_config():
    """检查 Redis 配置"""
    print("\n🔴 Redis 配置:")
    print(f"   主机: {settings.redis_host}")
    print(f"   端口: {settings.redis_port}")
    print(f"   数据库: {settings.redis_db}")
    if settings.redis_password:
        print(f"   密码: {'*' * len(settings.redis_password)}")
    print(f"   URL: {settings.redis_url}")


def test_redis_connection():
    """测试 Redis 连接"""
    print("\n🔍 测试 Redis 连接...")
    try:
        r = redis.from_url(settings.redis_url)
        r.ping()
        print("✅ Redis 连接成功")
        return True
    except Exception as e:
        print(f"❌ Redis 连接失败: {e}")
        return False


def check_other_configs():
    """检查其他配置"""
    print("\n⚙️  其他配置:")
    print(f"   JWT 密钥: {'*' * len(settings.secret_key)}")
    print(f"   Token 过期时间: {settings.access_token_expire_minutes} 分钟")
    print(f"   服务器地址: {settings.host}:{settings.port}")
    print(f"   调试模式: {settings.debug}")
    print(f"   CORS 允许源: {settings.allowed_origins}")


def main():
    """主函数"""
    print("🔧 Interview Express 配置检查工具")
    print("=" * 50)
    
    # 检查环境变量文件
    env_ok = check_env_file()
    
    # 检查数据库配置
    check_database_config()
    
    # 测试数据库连接
    db_ok = test_database_connection()
    
    # 检查 Redis 配置
    check_redis_config()
    
    # 测试 Redis 连接
    redis_ok = test_redis_connection()
    
    # 检查其他配置
    # check_other_configs()
    
    # 总结
    print("\n" + "=" * 50)
    print("📋 检查总结:")
    print(f"   环境变量文件: {'✅' if env_ok else '❌'}")
    print(f"   数据库连接: {'✅' if db_ok else '❌'}")
    print(f"   Redis 连接: {'✅' if redis_ok else '❌'}")
    
    if not env_ok:
        print("\n💡 建议:")
        print("   1. 复制 env.example 为 .env")
        print("   2. 编辑 .env 文件配置数据库和Redis连接信息")
    
    if not db_ok:
        print("\n💡 数据库问题:")
        print("   1. 确保 MySQL 服务已启动")
        print("   2. 检查 .env 中的数据库配置")
        print("   3. 确保数据库用户有足够权限")
    
    if not redis_ok:
        print("\n💡 Redis 问题:")
        print("   1. 确保 Redis 服务已启动")
        print("   2. 检查 .env 中的 Redis 配置")
    
    if env_ok and db_ok and redis_ok:
        print("\n🎉 所有配置检查通过！可以启动应用了。")
        return 0
    else:
        print("\n⚠️  存在配置问题，请根据上述建议进行修复。")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 