import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app
from app.services.sms_service import sms_service

# 测试数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_send_sms_code(setup_database):
    """测试发送短信验证码"""
    response = client.post("/api/v1/auth/send-code", params={"phone": "13800138000"})
    assert response.status_code == 200
    assert response.json()["message"] == "SMS code sent successfully"

def test_login_with_valid_code(setup_database):
    """测试使用有效验证码登录"""
    # 先发送验证码
    client.post("/api/v1/auth/send-code", params={"phone": "13800138000"})
    
    # 获取验证码（测试环境）
    code_response = client.get("/api/v1/auth/test-code/13800138000")
    code = code_response.json()["code"]
    
    # 登录
    login_data = {"phone": "13800138000", "code": code}
    response = client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["phone"] == "13800138000"

def test_login_with_invalid_code(setup_database):
    """测试使用无效验证码登录"""
    login_data = {"phone": "13800138000", "code": "123456"}
    response = client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 400
    assert "Invalid verification code" in response.json()["detail"] 