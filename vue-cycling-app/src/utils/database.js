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

  // 测试连接 - 检查后端服务是否可用
  static async testConnection() {
    try {
      // 优先尝试Python后端
      const pythonResponse = await pythonApiClient.get('/health');
      console.log('✅ Python后端服务连接成功:', pythonResponse.data);
      return true;
    } catch (pythonError) {
      console.log('⚠️ Python后端连接失败，尝试Java后端:', pythonError.message);
      try {
        const javaResponse = await apiClient.get('/health');
        console.log('✅ Java后端服务连接成功:', javaResponse.data);
        return true;
      } catch (javaError) {
        console.error('❌ 所有后端服务连接失败:', { python: pythonError.message, java: javaError.message });
        return false;
      }
    }
  }

  // Python后端API调用
  static async queryPython(endpoint, params = {}) {
    try {
      const response = await pythonApiClient.get(endpoint, { params });
      return response.data;
    } catch (error) {
      console.error('Python API查询错误:', error);
      throw error;
    }
  }

  static async insertPython(endpoint, data) {
    try {
      const response = await pythonApiClient.post(endpoint, data);
      return response.data;
    } catch (error) {
      console.error('Python API请求错误:', error);
      throw error;
    }
  }

  // 智能查询 - 自动选择可用的后端
  static async smartQuery(endpoint, params = {}) {
    try {
      // 如果是装备相关的查询，优先使用Python后端
      if (endpoint.includes('equipment') || endpoint.includes('categories')) {
        return await this.queryPython(endpoint, params);
      }
      // 其他查询优先使用Java后端
      return await this.query(endpoint, params);
    } catch (error) {
      console.log(`主要后端查询失败，尝试备用后端: ${error.message}`);
      try {
        // 如果主要后端失败，尝试另一个后端
        if (endpoint.includes('equipment') || endpoint.includes('categories')) {
          return await this.query(endpoint, params);
        } else {
          return await this.queryPython(endpoint, params);
        }
      } catch (fallbackError) {
        console.error('所有后端查询都失败:', fallbackError);
        throw fallbackError;
      }
    }
  }
}

export default Database;