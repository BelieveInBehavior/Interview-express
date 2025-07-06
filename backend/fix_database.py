#!/usr/bin/env python3
"""
修复数据库表结构脚本
"""

import os
import sys
from sqlalchemy import text

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_database():
    """修复数据库表结构"""
    try:
        from app.core.database import engine
        
        print("🔧 正在修复数据库表结构...")
        
        with engine.connect() as connection:
            # 检查users表是否存在
            result = connection.execute(text("SHOW TABLES LIKE 'users'"))
            if not result.fetchone():
                print("❌ users表不存在，请先创建表")
                return False
            
            # 检查updated_at字段是否有默认值
            result = connection.execute(text("""
                SELECT COLUMN_DEFAULT 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = 'interview_express' 
                AND TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'updated_at'
            """))
            
            row = result.fetchone()
            if row and row[0] is None:
                print("🔧 修复updated_at字段默认值...")
                connection.execute(text("""
                    ALTER TABLE users 
                    MODIFY COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                """))
                connection.commit()
                print("✅ updated_at字段已修复")
            else:
                print("✅ updated_at字段已正确配置")
        
        return True
        
    except Exception as e:
        print(f"❌ 修复数据库失败: {e}")
        return False

def recreate_tables():
    """重新创建表"""
    try:
        from app.core.database import engine, Base
        from app.models import User, Experience
        
        print("🔧 正在重新创建数据库表...")
        
        # 删除现有表
        with engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS experiences"))
            connection.execute(text("DROP TABLE IF EXISTS users"))
            connection.commit()
        
        # 重新创建表
        Base.metadata.create_all(bind=engine)
        
        print("✅ 数据库表重新创建成功")
        return True
        
    except Exception as e:
        print(f"❌ 重新创建表失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("数据库修复工具")
    print("=" * 50)
    
    choice = input("选择操作:\n1. 修复现有表结构\n2. 重新创建所有表\n请输入选择 (1 或 2): ")
    
    if choice == "1":
        if fix_database():
            print("\n✅ 数据库修复完成！")
        else:
            print("\n❌ 数据库修复失败！")
    elif choice == "2":
        if recreate_tables():
            print("\n✅ 数据库表重新创建完成！")
        else:
            print("\n❌ 数据库表重新创建失败！")
    else:
        print("❌ 无效选择") 