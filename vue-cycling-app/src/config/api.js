// API配置文件
// 统一管理所有后端服务的URL配置

// 环境配置
const isDev = import.meta.env.DEV;
const isProd = import.meta.env.PROD;

// 后端服务配置
export const API_CONFIG = {
  // Java后端服务 (主要API服务)
  JAVA_BACKEND: {
    baseURL: isDev ? '/api' : 'https://your-production-domain.com/api',
    timeout: 10000,
    description: 'Java后端 - 主要API服务、用户认证、路线规划等'
  },
  
  // Python后端服务 (爬虫服务)
  PYTHON_BACKEND: {
    baseURL: isDev ? 'http://localhost:5000/api' : 'https://your-python-backend.com/api',
    timeout: 15000,
    description: 'Python后端 - 爬虫服务、设备管理等'
  },
  
  // 路线规划服务 (Java后端的特定配置)
  ROUTE_PLANNING: {
    baseURL: isDev ? '/api' : 'https://your-production-domain.com/api',
    timeout: 30000, // 路线规划可能需要更长时间
    description: 'Java后端 - 路线规划专用配置'
  }
};

// 默认请求头配置
export const DEFAULT_HEADERS = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
};

// API端点配置
export const API_ENDPOINTS = {
  // 认证相关
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh'
  },
  
  // 用户相关
  USER: {
    PROFILE: '/user/profile',
    UPDATE_PROFILE: '/user/profile'
  },
  
  // 路线相关
  ROUTES: {
    LIST: '/routes',
    CREATE: '/routes',
    DETAIL: (id) => `/routes/${id}`,
    UPDATE: (id) => `/routes/${id}`,
    DELETE: (id) => `/routes/${id}`,
    SEARCH: '/routes/search'
  },
  
  // 路线规划相关 (Java后端)
  ROUTE_PLANNING: {
    PLAN: '/route/plan',
    QUICK_PLAN: '/route/quick-plan',
    GEOCODE: '/route/geocode',
    REVERSE_GEOCODE: '/route/reverse-geocode',
    TRANSPORT_MODES: '/route/transport-modes',
    STRATEGIES: '/route/strategies',
    HEALTH: '/route/health'
  },
  
  // 骑行记录相关
  RECORDS: {
    LIST: '/records',
    CREATE: '/records',
    STATS: '/records/stats'
  },
  
  // 反馈相关
  FEEDBACK: {
    SUBMIT: '/feedback',
    LIST: '/feedback'
  },
  
  // 数据库测试相关
  DATABASE: {
    HEALTH: '/health',
    TEST: '/test',
    TABLES: '/tables',
    CYCLING_ROUTES: '/cycling-routes'
  },
  
  // Python后端 - 爬虫服务
  CRAWLER: {
    STATUS: '/crawler/status',
    START: '/crawler/start',
    STOP: '/crawler/stop'
  },
  
  // Python后端 - 设备管理
  EQUIPMENT: {
    LIST: '/equipment',
    CREATE: '/equipment',
    UPDATE: (id) => `/equipment/${id}`,
    DELETE: (id) => `/equipment/${id}`
  }
};

// 错误码配置
export const ERROR_CODES = {
  NETWORK_ERROR: 'ERR_NETWORK',
  TIMEOUT: 'ECONNABORTED',
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  INTERNAL_SERVER_ERROR: 500
};

// 错误消息配置
export const ERROR_MESSAGES = {
  [ERROR_CODES.NETWORK_ERROR]: '网络连接失败，请检查网络设置',
  [ERROR_CODES.TIMEOUT]: '请求超时，请稍后重试',
  [ERROR_CODES.UNAUTHORIZED]: '登录已过期，请重新登录',
  [ERROR_CODES.FORBIDDEN]: '权限不足，无法访问该资源',
  [ERROR_CODES.NOT_FOUND]: '请求的资源不存在',
  [ERROR_CODES.INTERNAL_SERVER_ERROR]: '服务器内部错误，请稍后重试'
};

export default API_CONFIG;