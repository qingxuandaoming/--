<template>
  <main class="container">
    <div class="feedback-container">
      <div class="feedback-header">
        <h1>建议反馈</h1>
        <p>您的反馈是我们不断改进的动力，请告诉我们您的想法和建议</p>
      </div>
      
      <div class="feedback-types">
        <div 
          v-for="(type, index) in feedbackTypes" 
          :key="index"
          class="feedback-type" 
          :class="{ active: activeFeedbackType === type.id }"
          @click="activeFeedbackType = type.id"
        >
          <i :class="type.icon"></i>
          <h3>{{ type.title }}</h3>
        </div>
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="name">您的姓名</label>
          <input type="text" id="name" v-model="formData.name" placeholder="请输入您的姓名" required>
        </div>
        
        <div class="form-group">
          <label for="email">电子邮箱</label>
          <input type="email" id="email" v-model="formData.email" placeholder="请输入您的电子邮箱" required>
        </div>
        
        <div class="form-group">
          <label for="route">相关路线</label>
          <select id="route" v-model="formData.route">
            <option value="">-- 请选择相关路线 --</option>
            <option value="湖滨休闲道">湖滨休闲道</option>
            <option value="森林山地线">森林山地线</option>
            <option value="海岸风景道">海岸风景道</option>
            <option value="其他">其他</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>您的体验评分</label>
          <div class="rating-stars">
            <i 
              v-for="n in 5" 
              :key="n"
              class="fas fa-star" 
              :class="{ active: n <= formData.rating }"
              @click="formData.rating = n"
            ></i>
          </div>
        </div>
        
        <div class="form-group">
          <label for="feedback">您的反馈内容</label>
          <textarea id="feedback" v-model="formData.content" placeholder="请详细描述您的建议或问题..." required></textarea>
        </div>
        
        <div class="form-group">
          <label for="file">上传图片（可选）</label>
          <div class="file-upload">
            <button type="button" class="upload-btn">选择文件</button>
            <input type="file" id="file" @change="handleFileChange" accept="image/*">
          </div>
          <p class="file-name" v-if="formData.fileName">{{ formData.fileName }}</p>
        </div>
        
        <button type="submit" class="submit-btn">提交反馈</button>
      </form>
      
      <div class="feedback-footer">
        <p>感谢您的宝贵意见，我们会认真对待每一条反馈</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';

const activeFeedbackType = ref('suggestion');
const feedbackTypes = [
  { id: 'suggestion', title: '功能建议', icon: 'fas fa-lightbulb' },
  { id: 'bug', title: '问题反馈', icon: 'fas fa-bug' },
  { id: 'experience', title: '体验分享', icon: 'fas fa-heart' },
  { id: 'other', title: '其他', icon: 'fas fa-comment-dots' }
];

const formData = ref({
  name: '',
  email: '',
  route: '',
  rating: 0,
  content: '',
  file: null,
  fileName: ''
});

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    formData.value.file = file;
    formData.value.fileName = file.name;
  }
};

const handleSubmit = () => {
  // 这里实现提交反馈的逻辑
  console.log('提交的反馈:', {
    type: activeFeedbackType.value,
    ...formData.value
  });
  
  // 提交成功后重置表单
  activeFeedbackType.value = 'suggestion';
  formData.value = {
    name: '',
    email: '',
    route: '',
    rating: 0,
    content: '',
    file: null,
    fileName: ''
  };
  
  // 显示成功提示
  alert('感谢您的反馈！我们会尽快处理。');
};
</script>

<style scoped>
.feedback-container {
  max-width: 800px;
  margin: 60px auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.feedback-header {
  text-align: center;
  margin-bottom: 40px;
}

.feedback-header h1 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.feedback-header p {
  color: #7f8c8d;
  font-size: 1.1rem;
  max-width: 600px;
  margin: 0 auto;
}

.feedback-types {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.feedback-type {
  text-align: center;
  padding: 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid #eee;
}

.feedback-type:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border-color: #FF9800;
}

.feedback-type.active {
  border-color: #FF9800;
  background-color: rgba(255, 152, 0, 0.1);
}

.feedback-type i {
  font-size: 2rem;
  color: #F57C00;
  margin-bottom: 15px;
}

.feedback-type h3 {
  color: #2c3e50;
  margin-bottom: 10px;
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

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  transition: border 0.3s ease;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: #FF9800;
  outline: none;
}

.form-group textarea {
  min-height: 150px;
  resize: vertical;
}

.rating-stars {
  display: flex;
  gap: 10px;
  font-size: 1.5rem;
  margin-top: 10px;
}

.rating-stars i {
  color: #ddd;
  cursor: pointer;
  transition: color 0.3s ease;
}

.rating-stars i:hover,
.rating-stars i.active {
  color: #FFB300;
}

.file-upload {
  position: relative;
  overflow: hidden;
  margin-top: 10px;
  display: inline-block;
}

.upload-btn {
  padding: 10px 20px;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
}

.upload-btn:hover {
  background: #e9ecef;
}

.file-upload input[type="file"] {
  position: absolute;
  top: 0;
  right: 0;
  min-width: 100%;
  min-height: 100%;
  font-size: 100px;
  text-align: right;
  filter: alpha(opacity=0);
  opacity: 0;
  outline: none;
  cursor: pointer;
  display: block;
}

.file-name {
  margin-top: 10px;
  font-size: 0.9rem;
  color: #7f8c8d;
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

.feedback-footer {
  text-align: center;
  margin-top: 30px;
  color: #7f8c8d;
  font-size: 0.9rem;
}
</style>