import axios from 'axios';
import { API_CONFIG, DEFAULT_HEADERS, API_ENDPOINTS, ERROR_CODES, ERROR_MESSAGES } from '@/config/api.js';

// 创建axios实例 - Java后端
const api = axios.create({
  baseURL: API_CONFIG.JAVA_BACKEND.baseURL,
  timeout: API_CONFIG.JAVA_BACKEND.timeout,
  headers: DEFAULT_HEADERS
});

// 创建Python后端axios实例
const pythonApi = axios.create({
  baseURL: API_CONFIG.PYTHON_BACKEND.baseURL,
  timeout: API_CONFIG.PYTHON_BACKEND.timeout,
  headers: DEFAULT_HEADERS
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
      const status = error.response.status;
      const message = ERROR_MESSAGES[status] || error.response.data?.message || '未知错误';
      
      switch (status) {
        case ERROR_CODES.UNAUTHORIZED:
          // 未授权，清除token并跳转到登录页
          localStorage.removeItem('token');
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          localStorage.removeItem('userInfo');
          window.location.href = '/login';
          break;
        case ERROR_CODES.FORBIDDEN:
          console.error('权限不足:', message);
          break;
        case ERROR_CODES.NOT_FOUND:
          console.error('资源不存在:', message);
          break;
        case ERROR_CODES.INTERNAL_SERVER_ERROR:
          console.error('服务器错误:', message);
          break;
        default:
          console.error('请求失败:', message);
      }
    } else if (error.request) {
      const errorCode = error.code;
      const message = ERROR_MESSAGES[errorCode] || '网络错误，请检查网络连接';
      console.error(message);
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
    login: (credentials) => api.post(API_ENDPOINTS.AUTH.LOGIN, credentials),
    
    // 用户注册
    register: (userData) => api.post(API_ENDPOINTS.AUTH.REGISTER, userData),
    
    // 获取用户信息
    getProfile: () => api.get(API_ENDPOINTS.USER.PROFILE),
    
    // 更新用户信息
    updateProfile: (userData) => api.put(API_ENDPOINTS.USER.UPDATE_PROFILE, userData),
    
    // 用户登出
    logout: () => api.post(API_ENDPOINTS.AUTH.LOGOUT),
    
    // 刷新token
    refreshToken: () => api.post(API_ENDPOINTS.AUTH.REFRESH)
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

  // 创建路线规划专用axios实例（需要更长超时时间）
  static #routePlanningApi = axios.create({
    baseURL: API_CONFIG.ROUTE_PLANNING.baseURL,
    timeout: API_CONFIG.ROUTE_PLANNING.timeout,
    headers: DEFAULT_HEADERS
  });

  // 路线规划相关API (Java后端)
  static routePlanning = {
    // 完整路线规划
    planRoute: (routeData) => {
      return this.#routePlanningApi.post(API_ENDPOINTS.ROUTE_PLANNING.PLAN, routeData);
    },
    
    // 快速路线规划
    quickPlan: (origin, destination, transportMode, city = '石家庄') => {
      const params = new URLSearchParams({
        origin,
        destination,
        transportMode,
        city
      });
      return this.#routePlanningApi.get(`${API_ENDPOINTS.ROUTE_PLANNING.QUICK_PLAN}?${params}`);
    },
    
    // 地理编码（地址转坐标）
    geocode: (address, city = '石家庄') => {
      const params = new URLSearchParams({ address, city });
      return api.get(`${API_ENDPOINTS.ROUTE_PLANNING.GEOCODE}?${params}`);
    },
    
    // 逆地理编码（坐标转地址）
    reverseGeocode: (longitude, latitude) => {
      const params = new URLSearchParams({ longitude, latitude });
      return api.get(`${API_ENDPOINTS.ROUTE_PLANNING.REVERSE_GEOCODE}?${params}`);
    },
    
    // 获取支持的交通方式
    getTransportModes: () => {
      return api.get(API_ENDPOINTS.ROUTE_PLANNING.TRANSPORT_MODES);
    },
    
    // 获取路线策略
    getStrategies: () => {
      return api.get(API_ENDPOINTS.ROUTE_PLANNING.STRATEGIES);
    },
    
    // 健康检查
    healthCheck: () => {
      return api.get(API_ENDPOINTS.ROUTE_PLANNING.HEALTH);
    }
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
    submit: (feedbackData) => api.post(API_ENDPOINTS.FEEDBACK.SUBMIT, feedbackData),
    
    // 获取反馈列表（管理员）
    getAll: () => api.get(API_ENDPOINTS.FEEDBACK.LIST)
  };

  // Python后端 - 爬虫服务API
  static crawler = {
    // 获取爬虫状态
    getStatus: () => pythonApi.get(API_ENDPOINTS.CRAWLER.STATUS),
    
    // 启动爬虫
    start: (config = {}) => pythonApi.post(API_ENDPOINTS.CRAWLER.START, config),
    
    // 停止爬虫
    stop: () => pythonApi.post(API_ENDPOINTS.CRAWLER.STOP)
  };

  // Python后端 - 设备管理API
  static equipment = {
    // 获取设备列表
    getAll: (params = {}) => pythonApi.get(API_ENDPOINTS.EQUIPMENT.LIST, { params }),
    
    // 创建新设备
    create: (equipmentData) => pythonApi.post(API_ENDPOINTS.EQUIPMENT.CREATE, equipmentData),
    
    // 更新设备信息
    update: (id, equipmentData) => pythonApi.put(API_ENDPOINTS.EQUIPMENT.UPDATE(id), equipmentData),
    
    // 删除设备
    delete: (id) => pythonApi.delete(API_ENDPOINTS.EQUIPMENT.DELETE(id))
  };

  // 数据库测试相关API
  static database = {
    // 健康检查
    healthCheck: () => api.get(API_ENDPOINTS.DATABASE.HEALTH),
    
    // 基本测试
    test: () => api.get(API_ENDPOINTS.DATABASE.TEST),
    
    // 获取表列表
    getTables: () => api.get(API_ENDPOINTS.DATABASE.TABLES),
    
    // 获取骑行路线数据
    getCyclingRoutes: (params = {}) => api.get(API_ENDPOINTS.DATABASE.CYCLING_ROUTES, { params })
  };
}

export default ApiService;
export { api, pythonApi };