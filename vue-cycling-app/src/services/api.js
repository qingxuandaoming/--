import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:3000/api', // 后端API基础URL
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 可以在这里添加token等认证信息
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data;
  },
  error => {
    console.error('API请求错误:', error);
    
    // 处理不同的错误状态码
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          localStorage.removeItem('token');
          window.location.href = '/login';
          break;
        case 403:
          console.error('权限不足');
          break;
        case 404:
          console.error('请求的资源不存在');
          break;
        case 500:
          console.error('服务器内部错误');
          break;
        default:
          console.error('请求失败:', error.response.data.message || '未知错误');
      }
    } else if (error.request) {
      console.error('网络错误，请检查网络连接');
    } else {
      console.error('请求配置错误:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// API服务类
class ApiService {
  // 用户相关API
  static user = {
    // 用户登录
    login: (credentials) => api.post('/auth/login', credentials),
    
    // 用户注册
    register: (userData) => api.post('/auth/register', userData),
    
    // 获取用户信息
    getProfile: () => api.get('/user/profile'),
    
    // 更新用户信息
    updateProfile: (userData) => api.put('/user/profile', userData),
    
    // 用户登出
    logout: () => api.post('/auth/logout')
  };

  // 骑行路线相关API
  static routes = {
    // 获取所有路线
    getAll: () => api.get('/routes'),
    
    // 根据ID获取路线
    getById: (id) => api.get(`/routes/${id}`),
    
    // 创建新路线
    create: (routeData) => api.post('/routes', routeData),
    
    // 更新路线
    update: (id, routeData) => api.put(`/routes/${id}`, routeData),
    
    // 删除路线
    delete: (id) => api.delete(`/routes/${id}`),
    
    // 搜索路线
    search: (query) => api.get(`/routes/search?q=${encodeURIComponent(query)}`)
  };

  // 骑行记录相关API
  static records = {
    // 获取用户的骑行记录
    getUserRecords: () => api.get('/records'),
    
    // 创建骑行记录
    create: (recordData) => api.post('/records', recordData),
    
    // 获取骑行统计
    getStats: () => api.get('/records/stats')
  };

  // 反馈相关API
  static feedback = {
    // 提交反馈
    submit: (feedbackData) => api.post('/feedback', feedbackData),
    
    // 获取反馈列表（管理员）
    getAll: () => api.get('/feedback')
  };
}

export default ApiService;
export { api };