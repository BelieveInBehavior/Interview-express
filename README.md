# Interview Express - 面试经验分享平台

一个基于 React Native + FastAPI 的面试经验分享平台，支持用户注册、登录、发布和搜索面试经验。

## 🚀 项目特色

- **移动端**: React Native 跨平台应用
- **后端**: FastAPI + MySQL + Redis + Celery 分布式系统
- **认证**: 手机号 + 短信验证码登录
- **实时**: 异步任务处理和缓存
- **文档**: 完整的 API 文档

## 📁 项目结构

```
Interview-express/
├── frontend/                 # React Native 前端应用
│   ├── components/          # 可复用组件
│   ├── screens/            # 页面组件
│   ├── services/           # API 服务
│   ├── mock/               # Mock 数据（已移除）
│   └── ...
├── backend/                 # FastAPI 后端系统
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic 模式
│   │   ├── services/       # 业务逻辑
│   │   └── tasks/          # Celery 任务
│   ├── alembic/            # 数据库迁移
│   └── ...
├── start_backend.sh        # 后端启动脚本
└── README.md              # 项目说明
```

## 🛠️ 技术栈

### 前端 (React Native)
- React Native 0.79.5
- React Navigation
- Expo
- React Native Paper
- React Native Vector Icons

### 后端 (FastAPI)
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- MySQL 8.0
- Redis 7.0
- Celery 5.3.4
- Alembic (数据库迁移)
- JWT 认证

## 🚀 快速开始

### 环境要求

- Node.js 18+
- Python 3.11+
- MySQL 8.0+
- Redis 7.0+

### 1. 克隆项目

```bash
git clone <repository-url>
cd Interview-express
```

### 2. 启动后端

#### 方式一：使用启动脚本（推荐）

```bash
./start_backend.sh
```

#### 方式二：手动启动

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp env.example .env
# 编辑 .env 文件配置数据库连接

# 创建数据库
mysql -u root -p -e "CREATE DATABASE interview_express CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 运行数据库迁移
alembic upgrade head

# 启动服务
python run.py
```

### 3. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npx expo start
```

### 4. 启动 Celery Worker（可选）

```bash
cd backend
source venv/bin/activate
celery -A app.core.celery_app worker --loglevel=info
```

## 📱 功能特性

### 用户认证
- ✅ 手机号注册/登录
- ✅ 短信验证码验证
- ✅ JWT Token 认证
- ✅ 自动用户创建

### 面试经验管理
- ✅ 发布面试经验
- ✅ 经验列表展示
- ✅ 经验详情查看
- ✅ 经验搜索功能
- ✅ 难度评分系统

### 分布式特性
- ✅ 异步短信发送
- ✅ Redis 缓存验证码
- ✅ 任务队列处理
- ✅ 数据库连接池

## 🔧 配置说明

### 后端配置

编辑 `backend/.env` 文件：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/interview_express

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# JWT 配置
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 前端配置

编辑 `frontend/services/api.js` 文件中的 API 地址：

```javascript
const API_BASE_URL = 'http://localhost:8000/api/v1';
```

## 📖 API 文档

启动后端服务后，访问以下地址查看 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 主要 API 端点

#### 认证相关
- `POST /api/v1/auth/send-code` - 发送短信验证码
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/auth/test-code/{phone}` - 获取测试验证码

#### 经验相关
- `GET /api/v1/experiences` - 获取经验列表
- `GET /api/v1/experiences/{id}` - 获取单个经验
- `POST /api/v1/experiences` - 创建经验
- `PUT /api/v1/experiences/{id}` - 更新经验
- `DELETE /api/v1/experiences/{id}` - 删除经验
- `GET /api/v1/experiences/search/` - 搜索经验

## 🧪 测试

### 后端测试

```bash
cd backend
source venv/bin/activate
pytest
```

### 前端测试

```bash
cd frontend
npm test
```

## 🐳 Docker 部署

### 使用 Docker Compose

```bash
cd backend
docker-compose up -d
```

### 手动构建

```bash
# 构建后端镜像
cd backend
docker build -t interview-express-backend .

# 运行容器
docker run -p 8000:8000 interview-express-backend
```

## 📊 数据库设计

### 用户表 (users)
- `phone` (主键) - 手机号
- `username` - 用户名
- `avatar` - 头像
- `bio` - 个人简介
- `is_active` - 是否激活
- `created_at` - 创建时间
- `updated_at` - 更新时间

### 经验表 (experiences)
- `id` (主键) - 经验ID
- `company` - 公司名称
- `position` - 职位
- `summary` - 经验总结
- `content` - 详细内容
- `difficulty` - 难度评分
- `tags` - 标签（JSON格式）
- `user_phone` (外键) - 用户手机号
- `created_at` - 创建时间
- `updated_at` - 更新时间

## 🔒 安全特性

- JWT Token 认证
- 密码哈希存储
- 短信验证码验证
- CORS 配置
- 输入验证和清理

## 🚀 性能优化

- Redis 缓存验证码
- 数据库连接池
- 异步任务处理
- 分页查询
- 防抖搜索

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件
- 微信联系

---

**注意**: 这是一个演示项目，生产环境部署前请务必：
1. 修改默认密码和密钥
2. 配置真实的短信服务
3. 设置适当的 CORS 策略
4. 配置 HTTPS
5. 设置日志记录
6. 配置监控和告警