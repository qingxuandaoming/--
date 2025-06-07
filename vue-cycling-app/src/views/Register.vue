<template>
  <main class="container">
    <div class="auth-container">
      <div class="auth-header">
        <h1>创建账户</h1>
        <p>加入灵境骑行，探索更多精彩骑行路线</p>
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="username" placeholder="请输入用户名（3-20个字符）" required minlength="3" maxlength="20">
        </div>
        
        <div class="form-group">
          <label for="email">电子邮箱</label>
          <input type="email" id="email" v-model="email" placeholder="请输入您的电子邮箱" required>
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="password" @input="checkPasswordStrength" placeholder="请设置您的密码" required>
          
          <div class="password-requirements">
            <p>密码要求：</p>
            <ul>
              <li :class="{ valid: hasMinLength }">至少8个字符</li>
              <li :class="{ valid: hasNumber }">包含数字</li>
              <li :class="{ valid: hasLetter }">包含字母</li>
              <li :class="{ valid: hasSpecialChar }">包含特殊字符（推荐）</li>
            </ul>
          </div>
          
          <div class="password-strength">
            <div class="password-strength-bar" :style="{ width: passwordStrength + '%', background: passwordStrengthColor }"></div>
          </div>
          
          <div class="password-strength-text">密码强度：{{ passwordStrengthText }}</div>
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input type="password" id="confirmPassword" v-model="confirmPassword" placeholder="请再次输入您的密码" required>
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
        
        <div class="terms-checkbox">
          <input type="checkbox" id="terms" v-model="agreeTerms" required>
          <label for="terms">我已阅读并同意 <a href="#">服务条款</a> 和 <a href="#">隐私政策</a></label>
        </div>
        
        <button type="submit" class="submit-btn" :disabled="!agreeTerms || loading">
          <span v-if="loading">
            <i class="fas fa-spinner fa-spin"></i> 注册中...
          </span>
          <span v-else>注册</span>
        </button>
      </form>
      
      <div class="auth-footer">
        已有账户？ <router-link to="/login">立即登录</router-link>
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
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import ApiService from '@/services/api.js';

const router = useRouter();
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const agreeTerms = ref(false);
const passwordStrength = ref(0);
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

// 密码要求检查
const hasMinLength = computed(() => password.value.length >= 8);
const hasNumber = computed(() => /[0-9]/.test(password.value));
const hasLetter = computed(() => /[A-Za-z]/.test(password.value));
const hasSpecialChar = computed(() => /[^A-Za-z0-9]/.test(password.value));

const passwordStrengthColor = computed(() => {
  if (passwordStrength.value < 30) return '#e74c3c';
  if (passwordStrength.value < 60) return '#f39c12';
  return '#27ae60';
});

const passwordStrengthText = computed(() => {
  if (passwordStrength.value < 30) return '弱';
  if (passwordStrength.value < 60) return '中';
  return '强';
});

const checkPasswordStrength = () => {
  const pwd = password.value;
  let strength = 0;
  
  // 基础长度要求
  if (pwd.length >= 8) strength += 25;
  if (pwd.length >= 12) strength += 15;
  
  // 字符类型要求
  if (/[A-Za-z]/.test(pwd)) strength += 25; // 包含字母
  if (/[0-9]/.test(pwd)) strength += 25; // 包含数字
  if (/[^A-Za-z0-9]/.test(pwd)) strength += 10; // 包含特殊字符
  
  passwordStrength.value = Math.min(100, strength);
};

const handleSubmit = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';
    
    // 验证密码
    if (password.value !== confirmPassword.value) {
      errorMessage.value = '两次输入的密码不一致';
      return;
    }
    
    // 验证密码要求
    if (!hasMinLength.value) {
      errorMessage.value = '密码至少需要8个字符';
      return;
    }
    
    if (!hasNumber.value) {
      errorMessage.value = '密码必须包含数字';
      return;
    }
    
    if (!hasLetter.value) {
      errorMessage.value = '密码必须包含字母';
      return;
    }
    
    // 验证密码强度
    if (passwordStrength.value < 50) {
      errorMessage.value = '密码强度不足，请确保包含字母和数字，建议添加特殊字符';
      return;
    }
    
    const response = await ApiService.user.register({
      username: username.value,
      email: email.value,
      password: password.value,
      confirmPassword: confirmPassword.value
    });
    
    if (response.success) {
      successMessage.value = '注册成功！正在跳转到登录页面...';
      
      // 跳转到登录页
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    } else {
      errorMessage.value = response.message || '注册失败';
    }
  } catch (error) {
    console.error('注册错误:', error);
    errorMessage.value = error.response?.data?.message || '注册失败，请稍后重试';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-container {
  max-width: 500px;
  margin: 60px auto;
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

.form-row {
  display: flex;
  gap: 15px;
}

.form-row .form-group {
  flex: 1;
}

.password-strength {
  margin-top: 8px;
  height: 5px;
  background: #eee;
  border-radius: 3px;
  overflow: hidden;
}

.password-strength-bar {
  height: 100%;
  width: 0;
  transition: width 0.3s ease, background 0.3s ease;
}

.password-requirements {
  margin-top: 10px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 3px solid #FF9800;
}

.password-requirements p {
  margin: 0 0 8px 0;
  font-size: 0.9rem;
  font-weight: 500;
  color: #2c3e50;
}

.password-requirements ul {
  margin: 0;
  padding: 0;
  list-style: none;
}

.password-requirements li {
  font-size: 0.85rem;
  color: #7f8c8d;
  margin-bottom: 4px;
  padding-left: 20px;
  position: relative;
}

.password-requirements li::before {
  content: '✗';
  position: absolute;
  left: 0;
  color: #e74c3c;
  font-weight: bold;
}

.password-requirements li.valid {
  color: #27ae60;
}

.password-requirements li.valid::before {
  content: '✓';
  color: #27ae60;
}

.password-strength-text {
  font-size: 0.8rem;
  margin-top: 5px;
  color: #7f8c8d;
  font-weight: 500;
}

.terms-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-top: 20px;
}

.terms-checkbox input {
  margin-top: 5px;
}

.terms-checkbox label {
  font-size: 0.9rem;
  color: #7f8c8d;
  line-height: 1.4;
}

.terms-checkbox a {
  color: #E65100;
  text-decoration: none;
}

.terms-checkbox a:hover {
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

.terms-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 25px;
}

.terms-checkbox input {
  margin-top: 5px;
}

.terms-checkbox label {
  font-size: 0.9rem;
  color: #7f8c8d;
  line-height: 1.4;
}

.terms-checkbox a {
  color: #E65100;
  text-decoration: none;
}

.terms-checkbox a:hover {
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