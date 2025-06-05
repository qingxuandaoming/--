<template>
  <main class="container">
    <div class="auth-container">
      <div class="auth-header">
        <h1>创建账户</h1>
        <p>加入灵境骑行，探索更多精彩骑行路线</p>
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-row">
          <div class="form-group">
            <label for="firstName">姓</label>
            <input type="text" id="firstName" v-model="firstName" placeholder="请输入您的姓" required>
          </div>
          
          <div class="form-group">
            <label for="lastName">名</label>
            <input type="text" id="lastName" v-model="lastName" placeholder="请输入您的名" required>
          </div>
        </div>
        
        <div class="form-group">
          <label for="email">电子邮箱</label>
          <input type="email" id="email" v-model="email" placeholder="请输入您的电子邮箱" required>
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="password" @input="checkPasswordStrength" placeholder="请设置您的密码" required>
          
          <div class="password-strength">
            <div class="password-strength-bar" :style="{ width: passwordStrength + '%', background: passwordStrengthColor }"></div>
          </div>
          
          <div class="password-strength-text">{{ passwordStrengthText }}</div>
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input type="password" id="confirmPassword" v-model="confirmPassword" placeholder="请再次输入您的密码" required>
        </div>
        
        <div class="terms-checkbox">
          <input type="checkbox" id="terms" v-model="agreeTerms" required>
          <label for="terms">我已阅读并同意 <a href="#">服务条款</a> 和 <a href="#">隐私政策</a></label>
        </div>
        
        <button type="submit" class="submit-btn" :disabled="!agreeTerms">注册</button>
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

const firstName = ref('');
const lastName = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const agreeTerms = ref(false);
const passwordStrength = ref(0);

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
  
  if (pwd.length > 6) strength += 20;
  if (pwd.length > 10) strength += 10;
  if (/[A-Z]/.test(pwd)) strength += 20;
  if (/[0-9]/.test(pwd)) strength += 20;
  if (/[^A-Za-z0-9]/.test(pwd)) strength += 30;
  
  passwordStrength.value = Math.min(100, strength);
};

const handleSubmit = () => {
  // 这里实现注册逻辑
  if (password.value !== confirmPassword.value) {
    alert('两次输入的密码不一致');
    return;
  }
  
  console.log('注册信息:', {
    firstName: firstName.value,
    lastName: lastName.value,
    email: email.value,
    password: password.value,
    agreeTerms: agreeTerms.value
  });
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

.password-strength-text {
  font-size: 0.8rem;
  margin-top: 5px;
  color: #7f8c8d;
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
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 152, 0, 0.4);
}

.submit-btn:disabled {
  opacity: 0.7;
  transform: none;
  box-shadow: none;
  cursor: not-allowed;
}

.auth-footer {
  text-align: center;
  margin-top: 30px;
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