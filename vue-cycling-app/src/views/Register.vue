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
            <label for="username">用户名</label>
            <input type="text" id="username" v-model="username" placeholder="3-20个字符" required minlength="3" maxlength="20">
          </div>
          
          <div class="form-group">
            <label for="email">电子邮箱</label>
            <input type="email" id="email" v-model="email" placeholder="请输入邮箱" required>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="password">
              密码
              <button type="button" class="password-help-btn" @click="showPasswordModal = true">
                <i class="fas fa-question-circle"></i>
              </button>
            </label>
            <input type="password" id="password" v-model="password" @input="checkPasswordStrength" placeholder="请设置密码" required>
            
            <div class="password-strength">
              <div class="password-strength-bar" :style="{ width: passwordStrength + '%', background: passwordStrengthColor }"></div>
            </div>
            
            <div class="password-strength-text">强度：{{ passwordStrengthText }}</div>
          </div>
          
          <div class="form-group">
            <label for="confirmPassword">确认密码</label>
            <input type="password" id="confirmPassword" v-model="confirmPassword" placeholder="再次输入密码" required>
          </div>
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
    </div>
    
    <!-- 密码要求弹窗 -->
    <div v-if="showPasswordModal" class="modal-overlay" @click="showPasswordModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>密码要求</h3>
          <button class="close-btn" @click="showPasswordModal = false">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <div class="password-requirements-modal">
            <ul>
              <li :class="{ valid: hasMinLength }">
                <i class="fas" :class="hasMinLength ? 'fa-check-circle' : 'fa-times-circle'"></i>
                至少8个字符
              </li>
              <li :class="{ valid: hasNumber }">
                <i class="fas" :class="hasNumber ? 'fa-check-circle' : 'fa-times-circle'"></i>
                包含数字
              </li>
              <li :class="{ valid: hasLetter }">
                <i class="fas" :class="hasLetter ? 'fa-check-circle' : 'fa-times-circle'"></i>
                包含字母
              </li>
              <li :class="{ valid: hasSpecialChar }">
                <i class="fas" :class="hasSpecialChar ? 'fa-check-circle' : 'fa-times-circle'"></i>
                包含特殊字符（推荐）
              </li>
            </ul>
            <div class="password-tips">
              <p><strong>提示：</strong></p>
              <p>• 使用大小写字母、数字和特殊字符的组合</p>
              <p>• 避免使用常见密码如"123456"、"password"等</p>
              <p>• 不要使用个人信息作为密码</p>
            </div>
          </div>
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
const showPasswordModal = ref(false);

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
  max-width: 480px;
  margin: 40px auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.auth-header {
  text-align: center;
  margin-bottom: 25px;
}

.auth-header h1 {
  color: #2c3e50;
  margin-bottom: 8px;
  font-size: 1.8rem;
}

.auth-header p {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  color: #2c3e50;
  font-weight: 500;
}

.password-help-btn {
  background: none;
  border: none;
  color: #FF9800;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 2px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.password-help-btn:hover {
  color: #F57C00;
  transform: scale(1.1);
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
  gap: 20px;
  margin-bottom: 18px;
}

.form-row .form-group {
  flex: 1;
  margin-bottom: 0;
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
  font-size: 0.75rem;
  margin-top: 4px;
  color: #7f8c8d;
  font-weight: 500;
}

.terms-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin: 15px 0;
}

.terms-checkbox input {
  margin-top: 5px;
}

.terms-checkbox label {
  font-size: 0.85rem;
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
  padding: 12px;
  margin-top: 15px;
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

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 400px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px 15px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #7f8c8d;
  cursor: pointer;
  padding: 5px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  color: #e74c3c;
  background: #f8f9fa;
}

.modal-body {
  padding: 20px 25px;
}

.password-requirements-modal ul {
  list-style: none;
  padding: 0;
  margin: 0 0 20px 0;
}

.password-requirements-modal li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  font-size: 0.9rem;
  color: #7f8c8d;
  transition: color 0.3s ease;
}

.password-requirements-modal li.valid {
  color: #27ae60;
}

.password-requirements-modal li i {
  font-size: 1rem;
  width: 16px;
}

.password-requirements-modal .fa-check-circle {
  color: #27ae60;
}

.password-requirements-modal .fa-times-circle {
  color: #e74c3c;
}

.password-tips {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border-left: 3px solid #FF9800;
}

.password-tips p {
  margin: 0 0 8px 0;
  font-size: 0.85rem;
  color: #2c3e50;
  line-height: 1.4;
}

.password-tips p:last-child {
  margin-bottom: 0;
}

.password-tips strong {
  color: #FF9800;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .auth-container {
    margin: 20px;
    padding: 25px 20px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 0;
  }
  
  .form-row .form-group {
    margin-bottom: 18px;
  }
  
  .modal-content {
    width: 95%;
    margin: 20px;
  }
  
  .modal-header,
  .modal-body {
    padding: 15px 20px;
  }
}

</style>