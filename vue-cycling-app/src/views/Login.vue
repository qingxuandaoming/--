<template>
  <main class="container">
    <div class="auth-container">
      <div class="auth-header">
        <h1>欢迎回来</h1>
        <p>登录您的灵境骑行账户，探索更多精彩</p>
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="username"><i class="fas fa-user"></i> 用户名/邮箱</label>
          <input type="text" id="username" v-model="username" placeholder="请输入您的用户名或邮箱" required>
        </div>
        
        <div class="form-group">
          <label for="password"><i class="fas fa-lock"></i> 密码</label>
          <input type="password" id="password" v-model="password" placeholder="请输入您的密码" required>
        </div>
        
        <!-- 错误消息 -->
        <div v-if="errorMessage" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          {{ errorMessage }}
        </div>
        
        <!-- 成功消息 -->
        <div v-if="successMessage" class="success-message">
          <i class="fas fa-check-circle"></i>
          {{ successMessage }}
        </div>
        
        <div class="form-footer">
          <div class="remember-me">
            <input type="checkbox" id="remember" v-model="remember">
            <label for="remember">记住我</label>
          </div>
          
          <a href="#" class="forgot-password">忘记密码？</a>
        </div>
        
        <button type="submit" class="submit-btn" :disabled="loading">
          <span v-if="loading">
            <i class="fas fa-spinner fa-spin"></i> 登录中...
          </span>
          <span v-else>登录</span>
        </button>
      </form>
      
      <div class="auth-footer">
        还没有账户？ <router-link to="/register">立即注册</router-link>
      </div>
      
      <div class="social-login">
        <p>使用社交账号登录</p>
        
        <div class="social-icons">
          <a href="#" class="social-icon wechat">
            <i class="fab fa-weixin"></i>
          </a>
          
          <a href="#" class="social-icon weibo">
            <i class="fab fa-weibo"></i>
          </a>
          
          <a href="#" class="social-icon qq">
            <i class="fab fa-qq"></i>
          </a>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import ApiService from '@/services/api.js';

const router = useRouter();
const route = useRoute();
const username = ref('');
const password = ref('');
const remember = ref(false);
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const handleSubmit = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';
    
    const response = await ApiService.user.login({
      usernameOrEmail: username.value,
      password: password.value,
      remember: remember.value
    });
    
    if (response.success) {
      // 存储token
      localStorage.setItem('accessToken', response.accessToken);
      localStorage.setItem('refreshToken', response.refreshToken);
      
      // 存储用户信息
      localStorage.setItem('userInfo', JSON.stringify(response.user));
      
      // 显示成功消息
      successMessage.value = '登录成功！正在跳转...';
      
      // 获取重定向路径，如果没有则跳转到主页
      const redirectPath = route.query.redirect || '/';
      
      // 跳转到目标页面
      setTimeout(() => {
        router.push(redirectPath);
      }, 1000);
    } else {
      errorMessage.value = response.message || '登录失败';
    }
  } catch (error) {
    console.error('登录错误:', error);
    errorMessage.value = error.response?.data?.message || '登录失败，请稍后重试';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-container {
  max-width: 450px;
  margin: 80px auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-header h1 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.auth-header p {
  color: #7f8c8d;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #2c3e50;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  transition: border 0.3s ease;
}

.form-group input:focus {
  border-color: #FF9800;
  outline: none;
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
}

.forgot-password {
  color: #E65100;
  text-decoration: none;
}

.forgot-password:hover {
  text-decoration: underline;
}

.submit-btn {
  width: 100%;
  padding: 14px;
  margin-top: 20px;
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  background: linear-gradient(135deg, #2980b9, #1abc9c);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(52, 152, 219, 0.3);
}

.submit-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* 消息样式 */
.error-message {
  background: #fee;
  color: #e74c3c;
  padding: 12px;
  border-radius: 6px;
  border-left: 4px solid #e74c3c;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.success-message {
  background: #efe;
  color: #27ae60;
  padding: 12px;
  border-radius: 6px;
  border-left: 4px solid #27ae60;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.fa-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.auth-footer {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #ecf0f1;
  color: #7f8c8d;
}

.auth-footer a {
  color: #E65100;
  text-decoration: none;
  font-weight: 500;
}

.auth-footer a:hover {
  text-decoration: underline;
}

.social-login {
  margin-top: 30px;
  text-align: center;
}

.social-login p {
  margin-bottom: 15px;
  color: #7f8c8d;
  position: relative;
}

.social-login p::before,
.social-login p::after {
  content: "";
  position: absolute;
  top: 50%;
  width: 35%;
  height: 1px;
  background: #ddd;
}

.social-login p::before {
  left: 0;
}

.social-login p::after {
  right: 0;
}

.social-icons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.social-icon {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #2c3e50;
  transition: all 0.3s ease;
}

.social-icon:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.social-icon.wechat {
  color: #07C160;
}

.social-icon.weibo {
  color: #E6162D;
}

.social-icon.qq {
  color: #12B7F5;
}
</style>