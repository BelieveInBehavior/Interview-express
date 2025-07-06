# 面经快车后端服务

基于 FastAPI 的分布式后端系统，支持用户认证、经验分享、搜索等功能。

## 功能特性

- 🔐 **用户认证**: 支持直接登录（用户名+手机号）
- 📝 **经验管理**: 创建、编辑、删除、搜索经验
- 🔍 **智能搜索**: 支持关键词搜索和筛选
- 📱 **短信服务**: 集成阿里云短信服务（可选）
- 🚀 **高性能**: 异步处理，Redis缓存
- �� **容器化**: Docker支持
- 📊 **任务队列**: Celery异步任务处理

## 技术栈

- **Web框架**: FastAPI
- **数据库**: MySQL
- **缓存**: Redis
- **任务队列**: Celery
- **ORM**: SQLAlchemy
- **认证**: JWT
- **短信**: 阿里云短信服务（已禁用）
- **容器**: Docker & Docker Compose

## 项目结构

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # 认证相关API
│   │       └── experiences.py   # 经验相关API
│   ├── core/
│   │   ├── config.py            # 配置管理
│   │   ├── database.py          # 数据库连接
│   │   └── security.py          # 安全工具
│   ├── models/
│   │   ├── user.py              # 用户模型
│   │   └── experience.py        # 经验模型
│   ├── schemas/
│   │   ├── user.py              # 用户数据模式
│   │   └── experience.py        # 经验数据模式
│   ├── services/
│   │   ├── user_service.py      # 用户服务
│   │   ├── experience_service.py # 经验服务
│   │   ├── sms_service.py       # 短信服务（已禁用）
│   │   └── aliyun_sms_service.py # 阿里云短信服务（已禁用）
│   └── main.py                  # 主应用
├── tasks/
│   ├── celery_app.py            # Celery应用
│   └── tasks.py                 # 异步任务
├── tests/                       # 测试文件
├── alembic/                     # 数据库迁移
├── requirements.txt             # 依赖包
├── .env                         # 环境变量
├── docker-compose.yml           # Docker编排
└── Dockerfile                   # Docker镜像
```

## 快速开始

### 1. 环境准备

确保已安装：
- Python 3.8+
- MySQL 8.0+
- Redis 6.0+
- Docker (可选)

### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

复制环境变量模板：
```bash
cp env.local.example .env
```

编辑 `.env` 文件，配置数据库、Redis等参数。

### 4. 数据库初始化

```bash
# 创建数据库迁移
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 5. 启动服务

```bash
# 启动后端服务
python run.py

# 或使用uvicorn直接启动
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 验证服务

访问以下地址验证服务：
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## API接口

### 认证接口

#### 直接登录
```http
POST /api/v1/auth/direct-login
Content-Type: application/json

{
  "phone": "13800138000",
  "username": "用户名"
}
```

#### 验证码登录（可选）
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "phone": "13800138000",
  "username": "用户名",
  "code": "1234"
}
```

#### 发送验证码
```http
POST /api/v1/auth/send-code?phone=13800138000
```

### 经验接口

#### 获取经验列表
```http
GET /api/v1/experiences?page=1&size=10
```

#### 创建经验
```http
POST /api/v1/experiences
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "面试经验标题",
  "content": "面试经验内容",
  "company": "公司名称",
  "position": "职位名称"
}
```

#### 搜索经验
```http
GET /api/v1/experiences/search/?q=关键词&company=公司名
```

## 短信服务配置

### 阿里云短信服务（已禁用）

短信服务功能已被禁用，系统仅支持直接登录。

如需重新启用短信服务，请：
1. 取消注释相关API接口
2. 配置阿里云短信服务参数
3. 更新前端界面

### 测试功能

```bash
# 测试直接登录功能
python test_direct_login.py
```

## Docker部署

### 使用Docker Compose

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 单独构建镜像

```bash
# 构建后端镜像
docker build -t interview-express-backend .

# 运行容器
docker run -p 8000:8000 --env-file .env interview-express-backend
```

## 开发指南

### 代码规范

- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 遵循 PEP 8 规范

### 测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_auth.py
```

### 数据库迁移

```bash
# 创建迁移文件
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DATABASE_URL` | 数据库连接URL | - |
| `REDIS_URL` | Redis连接URL | - |
| `SECRET_KEY` | JWT密钥 | - |
| `ALGORITHM` | JWT算法 | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 访问令牌过期时间 | 30 |
| `SERVER_HOST` | 服务器主机 | 0.0.0.0 |
| `SERVER_PORT` | 服务器端口 | 8000 |
| `DEBUG` | 调试模式 | False |
| `ALLOWED_ORIGINS` | 允许的跨域来源 | ["*"] |

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务是否启动
   - 验证连接字符串是否正确
   - 确认数据库用户权限

2. **Redis连接失败**
   - 检查Redis服务是否启动
   - 验证Redis连接配置
   - 确认Redis端口是否开放

3. **JWT令牌无效**
   - 检查SECRET_KEY配置
   - 验证令牌是否过期
   - 确认令牌格式是否正确

### 日志查看

```bash
# 查看应用日志
tail -f logs/app.log

# 查看Celery日志
tail -f logs/celery.log
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License 