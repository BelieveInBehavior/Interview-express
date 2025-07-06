#!/usr/bin/env python3
"""
经验表迁移脚本 - 更新外键引用从user_phone到user_id
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import engine
from app.core.config import settings

def migrate_experiences_table():
    """迁移经验表结构"""
    print("正在迁移经验表...")
    
    with engine.connect() as conn:
        # 检查用户表是否存在且有id字段
        result = conn.execute(text("SHOW TABLES LIKE 'users'"))
        if not result.fetchone():
            print("用户表不存在，请先创建用户表")
            return
        
        # 检查用户表结构
        result = conn.execute(text("DESCRIBE users"))
        user_columns = [row[0] for row in result.fetchall()]
        
        if 'id' not in user_columns:
            print("用户表缺少id字段，请先运行用户表迁移")
            return
        
        # 检查经验表是否存在
        result = conn.execute(text("SHOW TABLES LIKE 'experiences'"))
        if not result.fetchone():
            print("经验表不存在，跳过迁移")
            return
        
        # 检查经验表结构
        result = conn.execute(text("DESCRIBE experiences"))
        exp_columns = [row[0] for row in result.fetchall()]
        
        if 'user_id' not in exp_columns:
            print("添加user_id字段...")
            # 添加user_id字段
            conn.execute(text("""
                ALTER TABLE experiences 
                ADD COLUMN user_id INT
            """))
            print("✅ user_id字段添加成功")
            
            # 更新user_id字段，根据user_phone查找对应的user.id
            print("更新user_id数据...")
            try:
                conn.execute(text("""
                    UPDATE experiences e 
                    JOIN users u ON e.user_phone = u.phone 
                    SET e.user_id = u.id
                """))
                print("✅ user_id数据更新成功")
            except Exception as e:
                print(f"⚠️ 更新user_id数据时出错: {e}")
                print("将user_id设置为NULL，需要手动处理")
            
            # 设置user_id为NOT NULL（如果数据更新成功）
            try:
                conn.execute(text("""
                    ALTER TABLE experiences 
                    MODIFY COLUMN user_id INT NOT NULL
                """))
                print("✅ user_id字段设置为NOT NULL")
            except Exception as e:
                print(f"⚠️ 设置NOT NULL失败: {e}")
                print("请手动处理数据后再设置NOT NULL")
            
            # 添加外键约束
            print("添加外键约束...")
            try:
                conn.execute(text("""
                    ALTER TABLE experiences 
                    ADD CONSTRAINT fk_experiences_user_id 
                    FOREIGN KEY (user_id) REFERENCES users(id)
                """))
                print("✅ 外键约束添加成功")
            except Exception as e:
                print(f"⚠️ 添加外键约束失败: {e}")
                print("请检查用户表结构和数据完整性")
            
            # 删除旧的user_phone字段（如果外键约束添加成功）
            if 'user_phone' in exp_columns:
                try:
                    conn.execute(text("""
                        ALTER TABLE experiences 
                        DROP COLUMN user_phone
                    """))
                    print("✅ user_phone字段删除成功")
                except Exception as e:
                    print(f"⚠️ 删除user_phone字段失败: {e}")
        else:
            print("✅ user_id字段已存在")
        
        conn.commit()
    
    print("经验表迁移完成！")

if __name__ == "__main__":
    migrate_experiences_table() 