import uvicorn
import subprocess
import sys
import os
from app.core.config import settings

def check_aliyun_config():
    """检查阿里云短信配置"""
    try:
        result = subprocess.run(
            [sys.executable, "check_aliyun_config.py"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0:
            print("✅ 阿里云短信配置检查通过")
            return True
        else:
            print("⚠️  阿里云短信配置检查失败，将使用模拟模式")
            print(result.stdout)
            return False
            
    except Exception as e:
        print(f"⚠️  阿里云配置检查异常: {e}")
        return False

if __name__ == "__main__":
    print("🚀 启动后端服务...")
    
    # 检查阿里云配置
    check_aliyun_config()
    
    print(f"📡 服务地址: http://{settings.host}:{settings.port}")
    print(f"🔧 调试模式: {'开启' if settings.debug else '关闭'}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    ) 