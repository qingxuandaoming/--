// 认证工具函数

/**
 * 检查用户是否已登录
 * @returns {boolean} 是否已登录
 */
export function isAuthenticated() {
  const token = localStorage.getItem('accessToken');
  const userInfo = localStorage.getItem('userInfo');
  return !!(token && userInfo);
}

/**
 * 获取当前用户信息
 * @returns {object|null} 用户信息对象或null
 */
export function getCurrentUser() {
  try {
    const userInfo = localStorage.getItem('userInfo');
    return userInfo ? JSON.parse(userInfo) : null;
  } catch (error) {
    console.error('解析用户信息失败:', error);
    return null;
  }
}

/**
 * 获取访问令牌
 * @returns {string|null} 访问令牌或null
 */
export function getAccessToken() {
  return localStorage.getItem('accessToken');
}

/**
 * 获取刷新令牌
 * @returns {string|null} 刷新令牌或null
 */
export function getRefreshToken() {
  return localStorage.getItem('refreshToken');
}

/**
 * 清除认证信息（登出）
 */
export function clearAuth() {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  localStorage.removeItem('userInfo');
}

/**
 * 设置认证信息
 * @param {string} accessToken 访问令牌
 * @param {string} refreshToken 刷新令牌
 * @param {object} userInfo 用户信息
 */
export function setAuth(accessToken, refreshToken, userInfo) {
  localStorage.setItem('accessToken', accessToken);
  localStorage.setItem('refreshToken', refreshToken);
  localStorage.setItem('userInfo', JSON.stringify(userInfo));
}