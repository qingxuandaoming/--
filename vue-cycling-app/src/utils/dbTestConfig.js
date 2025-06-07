// 数据库测试配置
export const DB_TEST_CONFIG = {
  // 是否启用自动测试（开发环境）
  enableAutoTest: true,
  
  // 测试延迟时间（毫秒）
  testDelay: 2000,
  
  // API端点配置
  endpoints: {
    health: '/route/health',
    test: '/test',
    tables: '/tables',
    cyclingRoutes: '/cycling-routes',
    feedback: '/feedback'
  },
  
  // 错误处理配置
  errorHandling: {
    logErrors: true,
    showUserFriendlyMessages: true
  }
};

export default DB_TEST_CONFIG;