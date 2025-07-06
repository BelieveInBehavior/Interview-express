const API_BASE_URL = 'http://localhost:8000/api/v1';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = null;
  }

  // 设置认证令牌
  setToken(token) {
    this.token = token;
  }

  // 获取请求头
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    return headers;
  }

  // 通用请求方法
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || '请求失败');
      }

      return data;
    } catch (error) {
      console.error('API请求错误:', error);
      throw error;
    }
  }

  // 发送短信验证码
  // async sendSmsCode(phone) {
  //   return this.request('/auth/send-code', {
  //     method: 'POST',
  //     body: JSON.stringify({ phone }),
  //   });
  // }

  // 登录（带验证码）
  async login(phone, username, code) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ phone, username, code }),
    });
    
    // 保存令牌
    this.setToken(response.access_token);
    return response;
  }

  // 直接登录（无需验证码）
  async directLogin(phone, username) {
    const response = await this.request('/auth/direct-login', {
      method: 'POST',
      body: JSON.stringify({ phone, username }),
    });
    
    // 保存令牌
    this.setToken(response.access_token);
    return response;
  }

  // 获取经验列表
  async getExperiences(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = `/experiences${queryString ? `?${queryString}` : ''}`;
    return this.request(endpoint);
  }

  // 获取单个经验
  async getExperience(id) {
    return this.request(`/experiences/${id}`);
  }

  // 创建经验
  async createExperience(experienceData) {
    return this.request('/experiences', {
      method: 'POST',
      body: JSON.stringify(experienceData),
    });
  }

  // 更新经验
  async updateExperience(id, experienceData) {
    return this.request(`/experiences/${id}`, {
      method: 'PUT',
      body: JSON.stringify(experienceData),
    });
  }

  // 删除经验
  async deleteExperience(id) {
    return this.request(`/experiences/${id}`, {
      method: 'DELETE',
    });
  }

  // 搜索经验
  async searchExperiences(query, params = {}) {
    const searchParams = { q: query, ...params };
    const queryString = new URLSearchParams(searchParams).toString();
    return this.request(`/experiences/search/?${queryString}`);
  }

  // 获取测试验证码（仅开发环境）
  // async getTestCode(phone) {
  //   return this.request(`/auth/test-code/${phone}`);
  // }
}

// 创建全局 API 服务实例
const apiService = new ApiService();

export default apiService; 