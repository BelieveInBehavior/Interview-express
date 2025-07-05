#!/bin/bash

echo "🚀 启动 Interview Express 后端系统..."

# 检查是否安装了 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    exit 1
fi

# 检查是否安装了 pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 未安装，请先安装 pip3"
    exit 1
fi

# 进入后端目录
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install -r requirements.txt

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "📝 创建环境变量文件..."
    cp env.example .env
    echo "⚠️  请编辑 .env 文件配置数据库和Redis连接信息"
    echo "   然后重新运行此脚本"
    exit 1
fi

# 运行配置检查
echo "🔧 检查配置..."
python check_config.py
if [ $? -ne 0 ]; then
    echo "❌ 配置检查失败，请修复配置问题后重试"
    exit 1
fi

# 检查数据库连接
echo "🔍 检查数据库连接..."
python -c "
import pymysql
from app.core.config import settings
try:
    # 使用配置中的数据库连接信息
    conn = pymysql.connect(
        host=settings.database_host,
        user=settings.database_user,
        password=settings.database_password,
        database=settings.database_name,
        port=settings.database_port
    )
    print('✅ 数据库连接成功')
    print(f'   主机: {settings.database_host}:{settings.database_port}')
    print(f'   数据库: {settings.database_name}')
    print(f'   用户: {settings.database_user}')
    conn.close()
except Exception as e:
    print(f'❌ 数据库连接失败: {e}')
    print('请检查 .env 文件中的数据库配置')
    print('确保 MySQL 服务已启动且配置正确')
    exit(1)
"

# 运行数据库迁移
echo "🗄️  运行数据库迁移..."
alembic upgrade head

# 启动 FastAPI 服务
echo "🌐 启动 FastAPI 服务..."
echo "📖 API 文档地址: http://localhost:8000/docs"
echo "🔗 健康检查: http://localhost:8000/health"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python run.py 