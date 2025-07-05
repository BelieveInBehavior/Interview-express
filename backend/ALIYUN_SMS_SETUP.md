# 阿里云短信服务配置指南

本文档介绍如何在项目中配置和使用阿里云短信服务进行短信验证码发送。

## 功能特性

- ✅ 集成阿里云短信服务API
- ✅ 自动降级到模拟模式（配置不完整时）
- ✅ 发送频率限制（1分钟内只能发送一次）
- ✅ 验证码5分钟过期
- ✅ 详细的错误处理和日志记录
- ✅ 支持查询发送状态和详情

## 配置步骤

### 1. 阿里云控制台配置

#### 1.1 获取Access Key
1. 登录阿里云控制台：https://console.aliyun.com/
2. 进入"访问控制" -> "AccessKey管理"
3. 创建AccessKey，获取AccessKey ID和AccessKey Secret
4. 确保AccessKey有短信服务权限

#### 1.2 创建短信签名
1. 进入短信服务控制台：https://dysms.console.aliyun.com/
2. 点击"国内消息" -> "签名管理"
3. 创建新签名，填写签名名称和用途说明
4. 等待审核通过（通常1-2个工作日）

#### 1.3 创建短信模板
1. 点击"模板管理"
2. 创建新模板，选择"验证码"类型
3. 模板内容示例：
   ```
   您的验证码是：${code}，5分钟内有效，请勿泄露给他人。
   ```
4. 等待审核通过（通常1-2个工作日）

### 2. 项目配置

#### 2.1 安装依赖
```bash
pip install -r requirements.txt
```

#### 2.2 配置环境变量
复制 `env.local.example` 为 `.env` 并修改配置：

```bash
cp env.local.example .env
```

编辑 `.env` 文件，填入阿里云配置：

```env
# 阿里云短信服务配置
ALIYUN_ACCESS_KEY_ID=your_access_key_id
ALIYUN_ACCESS_KEY_SECRET=your_access_key_secret
ALIYUN_SMS_SIGN_NAME=your_sign_name
ALIYUN_SMS_TEMPLATE_CODE=SMS_123456789
ALIYUN_SMS_REGION_ID=cn-hangzhou
```

#### 2.3 验证配置
运行配置检查脚本：

```bash
python check_aliyun_config.py
```

## API 使用

### 发送验证码
```http
POST /api/v1/auth/send-code?phone=13800138000
```

响应示例：
```json
{
  "message": "验证码发送成功",
  "success": true,
  "request_id": "1234567890",
  "biz_id": "6789012345"
}
```

### 用户登录
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "phone": "13800138000",
  "code": "123456"
}
```

### 查询发送状态
```http
GET /api/v1/auth/send-status/13800138000
```

响应示例：
```json
{
  "phone": "13800138000",
  "has_code": true,
  "has_frequency_limit": false,
  "code_ttl": 240,
  "frequency_ttl": 0
}
```

### 获取测试验证码（开发环境）
```http
GET /api/v1/auth/test-code/13800138000
```

## 错误处理

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `isv.INVALID_PARAMETERS` | 参数错误 | 检查手机号格式和模板参数 |
| `isv.INVALID_SIGN_NAME` | 签名不存在 | 检查签名是否已审核通过 |
| `isv.INVALID_TEMPLATE_CODE` | 模板不存在 | 检查模板是否已审核通过 |
| `isv.INSUFFICIENT_BALANCE` | 余额不足 | 充值短信服务 |
| `isv.MOBILE_NUMBER_ILLEGAL` | 手机号不合法 | 检查手机号格式 |

### 频率限制
- 同一手机号1分钟内只能发送一次验证码
- 验证码5分钟内有效
- 超过限制会返回429状态码

## 开发模式

当阿里云配置不完整时，系统会自动切换到模拟模式：

1. 验证码会打印到控制台日志
2. 可以通过 `/api/v1/auth/test-code/{phone}` 获取验证码
3. 所有功能正常工作，只是不发送真实短信

## 监控和日志

### 日志记录
系统会记录以下信息：
- 短信发送成功/失败
- 验证码验证结果
- 频率限制触发
- 异常错误信息

### 查询发送详情
```python
from app.services.aliyun_sms_service import aliyun_sms_service

# 查询发送详情
result = aliyun_sms_service.query_send_details(
    phone="13800138000",
    send_date="20231201",
    page_size=10,
    current_page=1
)
```

## 安全注意事项

1. **Access Key安全**
   - 不要在代码中硬编码Access Key
   - 使用环境变量或配置文件
   - 定期轮换Access Key

2. **验证码安全**
   - 验证码5分钟过期
   - 验证成功后立即删除
   - 限制发送频率防止滥用

3. **手机号验证**
   - 验证手机号格式
   - 考虑添加手机号黑名单
   - 监控异常发送行为

## 故障排除

### 配置检查失败
1. 运行 `python check_aliyun_config.py`
2. 检查所有必需配置项
3. 确认Access Key权限

### 发送失败
1. 检查网络连接
2. 确认签名和模板已审核通过
3. 检查账户余额
4. 查看错误日志

### 验证码不匹配
1. 检查Redis连接
2. 确认验证码未过期
3. 检查手机号格式

## 相关链接

- [阿里云短信服务文档](https://help.aliyun.com/product/44282.html)
- [短信服务控制台](https://dysms.console.aliyun.com/)
- [API参考文档](https://help.aliyun.com/document_detail/101414.html)
- [错误码说明](https://help.aliyun.com/document_detail/101346.html) 