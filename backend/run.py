#!/usr/bin/env python3
"""
启动脚本 - 包含配置检查、数据库迁移和服务器启动
"""
import os
import sys
import subprocess
import time

def run_command(command, description):
    """运行命令并显示结果"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description}成功")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description}失败")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description}异常: {e}")
        return False
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 面经快车后端启动脚本")
    print("=" * 60)
    
    # 1. 检查配置
    if not run_command("python check_config.py", "检查配置"):
        print("\n❌ 配置检查失败，请检查.env文件")
        return
    
    # 2. 创建数据库表
    if not run_command("python create_tables.py", "创建数据库表"):
        print("\n❌ 数据库表创建失败")
        return
    
    # 3. 运行用户表迁移（如果存在）
    if os.path.exists("migrate_users_table.py"):
        if not run_command("python migrate_users_table.py", "运行用户表迁移"):
            print("\n❌ 用户表迁移失败")
            return
    
    # 4. 运行经验表迁移（如果存在）
    if os.path.exists("migrate_experiences_table.py"):
        if not run_command("python migrate_experiences_table.py", "运行经验表迁移"):
            print("\n❌ 经验表迁移失败")
            return
    
    # 5. 启动服务器
    print("\n🚀 启动FastAPI服务器...")
    print("📝 API文档地址: http://localhost:8000/docs")
    print("📝 服务器地址: http://localhost:8000")
    print("⏹️  按 Ctrl+C 停止服务器")
    print("-" * 60)
    
    try:
        # 启动uvicorn服务器
        subprocess.run([
            "uvicorn", "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 服务器启动失败: {e}")

if __name__ == "__main__":
    main() 