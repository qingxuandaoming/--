import axios from 'axios';

// API基础URL配置
const API_BASE_URL = 'http://localhost:8080/api'; // Java后端
const PYTHON_API_BASE_URL = 'http://localhost:5000/api'; // Python后端

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

const pythonApiClient = axios.create({
  baseURL: PYTHON_API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// API数据库操作类
class Database {
  // 执行查询 - 通过API调用后端
  static async query(endpoint, params = {}) {
    try {
      const response = await apiClient.get(endpoint, { params });
      return response.data;
    } catch (error) {
      console.error('API查询错误:', error);
      throw error;
    }
  }

  // 执行插入操作 - 通过API调用后端
  static async insert(endpoint, data) {
    try {
      const response = await apiClient.post(endpoint, data);
      return response.data;
    } catch (error) {
      console.error('API插入错误:', error);
      throw error;
    }
  }

  // 执行更新操作 - 通过API调用后端
  static async update(endpoint, data) {
    try {
      const response = await apiClient.put(endpoint, data);
      return response.data;
    } catch (error) {
      console.error('API更新错误:', error);
      throw error;
    }
  }

  // 执行删除操作 - 通过API调用后端
  static async delete(endpoint, params = {}) {
    try {
      const response = await apiClient.delete(endpoint, { params });
      return response.data;
    } catch (error) {
      console.error('API删除错误:', error);
      throw error;
    }
  }

  // 测试后端连接
  static async testConnection() {
    try {
      const response = await apiClient.get('/health');
      console.log('后端服务连接成功!');
      return response.data;
    } catch (error) {
      console.error('后端服务连接失败:', error);
      return false;
    }
  }

  // Python后端API调用
  static async pythonQuery(endpoint, params = {}) {
    try {
      const response = await pythonApiClient.get(endpoint, { params });
      return response.data;
    } catch (error) {
      console.error('Python API查询错误:', error);
      throw error;
    }
  }

  static async pythonPost(endpoint, data) {
    try {
      const response = await pythonApiClient.post(endpoint, data);
      return response.data;
    } catch (error) {
      console.error('Python API请求错误:', error);
      throw error;
    }
  }
}

export default Database;