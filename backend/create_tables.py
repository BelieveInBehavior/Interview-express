#!/usr/bin/env python3
"""
创建数据库表的脚本
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from app.models import Base
from app.core.config import settings

def create_tables():
    """创建所有数据库表"""
    print("正在创建数据库表...")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    print("数据库表创建完成！")
    print(f"数据库连接: {settings.database_url}")

if __name__ == "__main__":
    create_tables() 