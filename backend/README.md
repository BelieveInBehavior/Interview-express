# Interview Express Backend

基于 Python、FastAPI、MySQL、Redis、Celery 的面试经验分享平台后端系统。

## 技术栈

- **Web框架**: FastAPI
- **数据库**: MySQL
- **缓存**: Redis
- **任务队列**: Celery
- **ORM**: SQLAlchemy
- **数据库迁移**: Alembic
- **认证**: JWT
- **短信服务**: 阿里云短信服务
- **API文档**: Swagger/OpenAPI

## 项目结构

```
backend/
├── app/
│   ├── api/                 # API路由
│   │   ├── deps.py         # 依赖注入
│   │   └── v1/             # API版本1
│   │       ├── auth.py     # 认证相关API
│   │       └── experiences.py # 经验相关API
│   ├── core/               # 核心配置
│   │   ├── config.py       # 配置管理
│   │   ├── database.py     # 数据库连接
│   │   ├── security.py     # 安全相关
│   │   └── celery_app.py   # Celery配置
│   ├── models/             # 数据模型
│   │   ├── user.py         # 用户模型
│   │   └── experience.py   # 经验模型
│   ├── schemas/            # Pydantic模式
│   │   ├── user.py         # 用户模式
│   │   └── experience.py   # 经验模式
│   ├── services/           # 业务逻辑
│   │   ├── user_service.py # 用户服务
│   │   ├── experience_service.py # 经验服务
│   │   ├── sms_service.py  # 短信服务
│   │   └── aliyun_sms_service.py # 阿里云短信服务
│   ├── tasks/              # Celery任务
│   │   └── sms_tasks.py    # 短信任务
│   └── main.py             # 主应用
├── alembic/                # 数据库迁移
├── tests/                  # 测试
├── requirements.txt        # 依赖
├── env.example             # 环境变量示例
├── env.local.example       # 本地开发环境变量示例
├── run.py                  # 启动脚本
├── start_celery.py         # Celery启动脚本
├── check_config.py         # 配置检查脚本
├── check_aliyun_config.py  # 阿里云配置检查脚本
├── test_sms.py             # 短信功能测试脚本
└── ALIYUN_SMS_SETUP.md     # 阿里云短信配置指南
```

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 环境配置

复制环境变量文件并修改配置：

```bash
# 复制基础配置
cp env.example .env

# 或者复制本地开发配置（推荐）
cp env.local.example .env
```

编辑 `.env` 文件，配置数据库、Redis和短信服务信息：

#### 数据库配置方式

**方式一：分别配置（推荐）**
```env
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=your_password
DATABASE_NAME=interview_express
DATABASE_TEST_NAME=interview_express_test
```

**方式二：直接URL**
```env
DATABASE_URL_DIRECT=mysql+pymysql://user:password@host:port/database
```

#### Redis配置方式

**方式一：分别配置（推荐）**
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
# REDIS_PASSWORD=your_redis_password
```

**方式二：直接URL**
```env
REDIS_URL=redis://:password@host:port/db
```

#### 阿里云短信服务配置

```env
# 阿里云短信服务配置
ALIYUN_ACCESS_KEY_ID=your_access_key_id
ALIYUN_ACCESS_KEY_SECRET=your_access_key_secret
ALIYUN_SMS_SIGN_NAME=your_sign_name
ALIYUN_SMS_TEMPLATE_CODE=SMS_123456789
ALIYUN_SMS_REGION_ID=cn-hangzhou
```

> 📝 **注意**: 如果不配置阿里云短信服务，系统会自动使用模拟模式，验证码会打印到控制台日志中。

### 3. 数据库设置

创建数据库：

```sql
CREATE DATABASE interview_express CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

运行数据库迁移：

```bash
alembic upgrade head
```

### 4. 配置检查

在启动服务前，可以运行配置检查工具：

```bash
# 检查基础配置
python check_config.py

# 检查阿里云短信配置
python check_aliyun_config.py
```

这些工具会检查：
- 环境变量文件是否存在
- 数据库连接是否正常
- Redis 连接是否正常
- 阿里云短信服务配置是否正确
- 其他配置是否正确

### 5. 启动服务

#### 启动 FastAPI 服务

```bash
python run.py
```

或者使用 uvicorn：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 启动 Celery Worker

```bash
celery -A app.core.celery_app worker --loglevel=info
```

#### 启动 Celery Beat（定时任务）

```bash
celery -A app.core.celery_app beat --loglevel=info
```

## API 文档

启动服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 主要功能

### 用户认证
- 手机号注册/登录
- 短信验证码验证（支持阿里云短信服务）
- JWT Token 认证
- 发送频率限制（1分钟内只能发送一次）

### 面试经验管理
- 创建、更新、删除经验
- 经验列表和搜索
- 标签管理

### 分布式特性
- 异步短信发送
- 任务队列处理
- Redis 缓存

### 短信服务特性
- ✅ 集成阿里云短信服务API
- ✅ 自动降级到模拟模式（配置不完整时）
- ✅ 发送频率限制（1分钟内只能发送一次）
- ✅ 验证码5分钟过期
- ✅ 详细的错误处理和日志记录
- ✅ 支持查询发送状态和详情

## 短信服务配置

### 阿里云短信服务

系统支持阿里云短信服务进行真实的短信验证码发送。详细配置说明请参考：[ALIYUN_SMS_SETUP.md](ALIYUN_SMS_SETUP.md)

#### 快速配置步骤：

1. **获取阿里云Access Key**
   - 登录阿里云控制台：https://console.aliyun.com/
   - 进入"访问控制" -> "AccessKey管理"
   - 创建AccessKey，获取AccessKey ID和AccessKey Secret

2. **创建短信签名和模板**
   - 进入短信服务控制台：https://dysms.console.aliyun.com/
   - 创建短信签名并等待审核通过
   - 创建短信模板并等待审核通过

3. **配置环境变量**
   ```env
   ALIYUN_ACCESS_KEY_ID=your_access_key_id
   ALIYUN_ACCESS_KEY_SECRET=your_access_key_secret
   ALIYUN_SMS_SIGN_NAME=your_sign_name
   ALIYUN_SMS_TEMPLATE_CODE=SMS_123456789
   ALIYUN_SMS_REGION_ID=cn-hangzhou
   ```

4. **验证配置**
   ```bash
   python check_aliyun_config.py
   ```

### 模拟模式

当阿里云配置不完整时，系统会自动切换到模拟模式：

- 验证码会打印到控制台日志
- 可以通过 `/api/v1/auth/test-code/{phone}` 获取验证码
- 所有功能正常工作，只是不发送真实短信

## 测试

### 短信功能测试

运行短信功能测试脚本：

```bash
python test_sms.py
```

这个脚本会测试：
- 短信验证码发送
- 发送状态查询
- 验证码获取
- 用户登录
- 短信服务直接调用

### 单元测试

```bash
pytest
```

## 开发指南

### 创建新的数据库迁移

```bash
alembic revision --autogenerate -m "描述"
alembic upgrade head
```

### 代码格式化

```bash
# 使用 black 格式化代码
black app/

# 使用 isort 排序导入
isort app/
```

### 日志查看

系统使用Python标准logging模块，日志级别可以通过环境变量配置：

```env
LOG_LEVEL=INFO
```

## 部署

### Docker 部署

```bash
# 构建镜像
docker build -t interview-express-backend .

# 运行容器
docker-compose up -d
```

### 生产环境配置

1. 修改 `.env` 文件中的配置
2. 设置 `DEBUG=False`
3. 配置生产环境的数据库和Redis
4. 配置阿里云短信服务
5. 设置安全的 `SECRET_KEY`

## 故障排除

### 常见问题

1. **短信发送失败**
   - 检查阿里云配置是否正确
   - 确认签名和模板已审核通过
   - 检查账户余额

2. **验证码不匹配**
   - 检查Redis连接
   - 确认验证码未过期
   - 检查手机号格式

3. **频率限制**
   - 同一手机号1分钟内只能发送一次
   - 等待1分钟后重试

### 获取帮助

- 查看日志文件
- 运行配置检查脚本
- 参考阿里云短信服务文档
- 查看API文档

## 许可证

MIT License 