#!/usr/bin/env python3
"""
用户表迁移脚本 - 添加id字段并修改username为必填
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import engine
from app.core.config import settings

def migrate_users_table():
    """迁移用户表结构"""
    print("正在迁移用户表...")
    
    with engine.connect() as conn:
        # 检查表是否存在
        result = conn.execute(text("SHOW TABLES LIKE 'users'"))
        if not result.fetchone():
            print("用户表不存在，请先运行 create_tables.py")
            return
        
        # 检查是否已有id字段
        result = conn.execute(text("DESCRIBE users"))
        columns = [row[0] for row in result.fetchall()]
        
        if 'id' not in columns:
            print("添加id字段...")
            # 添加id字段作为主键
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST
            """))
            print("✅ id字段添加成功")
        else:
            print("✅ id字段已存在")
        
        # 修改username字段为NOT NULL
        result = conn.execute(text("""
            SELECT IS_NULLABLE, COLUMN_DEFAULT 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'users' AND COLUMN_NAME = 'username'
        """))
        username_info = result.fetchone()
        
        if username_info and username_info[0] == 'YES':
            print("修改username字段为必填...")
            # 先为空的username设置默认值
            conn.execute(text("""
                UPDATE users 
                SET username = CONCAT('user_', id) 
                WHERE username IS NULL OR username = ''
            """))
            
            # 修改字段为NOT NULL
            conn.execute(text("""
                ALTER TABLE users 
                MODIFY COLUMN username VARCHAR(50) NOT NULL
            """))
            print("✅ username字段修改为必填成功")
        else:
            print("✅ username字段已经是必填")
        
        # 添加唯一索引到phone字段（如果不存在）
        result = conn.execute(text("""
            SHOW INDEX FROM users WHERE Key_name = 'ix_users_phone'
        """))
        if not result.fetchone():
            print("添加phone字段唯一索引...")
            conn.execute(text("""
                ALTER TABLE users 
                ADD UNIQUE INDEX ix_users_phone (phone)
            """))
            print("✅ phone字段唯一索引添加成功")
        else:
            print("✅ phone字段唯一索引已存在")
        
        conn.commit()
    
    print("用户表迁移完成！")

if __name__ == "__main__":
    migrate_users_table() 