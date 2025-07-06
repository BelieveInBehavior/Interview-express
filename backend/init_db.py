#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建所有数据库表
"""

import os
import sys
from sqlalchemy import text

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.models import User, Experience  # 导入所有模型以确保它们被注册

def init_database():
    """初始化数据库，创建所有表"""
    print("🔧 正在初始化数据库...")
    
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建成功")
        
        # 验证表是否创建成功
        with engine.connect() as connection:
            # 检查users表
            result = connection.execute(text("SHOW TABLES LIKE 'users'"))
            if result.fetchone():
                print("✅ users表创建成功")
            else:
                print("❌ users表创建失败")
            
            # 检查experiences表
            result = connection.execute(text("SHOW TABLES LIKE 'experiences'"))
            if result.fetchone():
                print("✅ experiences表创建成功")
            else:
                print("❌ experiences表创建失败")
                
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False
    
    return True

def check_database_connection():
    """检查数据库连接"""
    print("🔍 检查数据库连接...")
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ 数据库连接成功")
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("数据库初始化工具")
    print("=" * 60)
    
    # 检查数据库连接
    if not check_database_connection():
        print("\n请检查以下配置：")
        print("1. 确保MySQL服务正在运行")
        print("2. 确保数据库 'interview_express' 已创建")
        print("3. 检查 .env 文件中的数据库配置")
        print("4. 确保数据库用户有创建表的权限")
        return
    
    # 初始化数据库
    if init_database():
        print("\n" + "=" * 60)
        print("数据库初始化完成")
        print("=" * 60)
        print("✅ 所有表已创建")
        print("📝 现在可以运行应用程序了")
    else:
        print("\n❌ 数据库初始化失败")
        print("请检查错误信息并重试")

if __name__ == "__main__":
    main() 