<template>
  <div class="safety-guide">
    <!-- 页面头部 -->
    <section class="hero safety-hero">
      <div class="hero-content">
        <h1>安全骑行指南</h1>
        <p>掌握正确骑行姿势与道路安全规范，让每一次骑行都安全无忧</p>
        <div class="hero-stats">
          <div class="stat-item">
            <i class="fas fa-shield-alt"></i>
            <span>安全第一</span>
          </div>
          <div class="stat-item">
            <i class="fas fa-user-graduate"></i>
            <span>专业指导</span>
          </div>
          <div class="stat-item">
            <i class="fas fa-heart"></i>
            <span>健康骑行</span>
          </div>
        </div>
      </div>
    </section>

    <main class="container">
      <!-- 基础安全知识 -->
      <section class="safety-section">
        <h2 class="section-title">
          <i class="fas fa-exclamation-triangle"></i>
          基础安全知识
        </h2>
        <div class="safety-grid">
          <div class="safety-card">
            <div class="card-icon">
              <i class="fas fa-hard-hat"></i>
            </div>
            <h3>头盔佩戴</h3>
            <p>正确佩戴头盔是骑行安全的第一要务。头盔应紧贴头部，下颌带调节至舒适但不松动的状态。</p>
            <ul>
              <li>选择符合安全标准的头盔</li>
              <li>确保头盔尺寸合适</li>
              <li>定期检查头盔完整性</li>
              <li>发生碰撞后及时更换</li>
            </ul>
          </div>
          
          <div class="safety-card">
            <div class="card-icon">
              <i class="fas fa-eye"></i>
            </div>
            <h3>视线安全</h3>
            <p>保持良好的视线是预防事故的关键。时刻观察路况，预判潜在危险。</p>
            <ul>
              <li>保持前方视线开阔</li>
              <li>定期检查后视镜</li>
              <li>注意盲区安全</li>
              <li>夜间使用照明设备</li>
            </ul>
          </div>
          
          <div class="safety-card">
            <div class="card-icon">
              <i class="fas fa-tshirt"></i>
            </div>
            <h3>着装要求</h3>
            <p>合适的骑行服装不仅提升舒适度，更能在关键时刻保护您的安全。</p>
            <ul>
              <li>穿着鲜艳醒目的服装</li>
              <li>选择透气排汗材质</li>
              <li>佩戴反光条或装备</li>
              <li>避免宽松易缠绕衣物</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- 道路安全规则 -->
      <section class="safety-section">
        <h2 class="section-title">
          <i class="fas fa-road"></i>
          道路安全规则
        </h2>
        <div class="rules-container">
          <div class="rule-item">
            <div class="rule-number">01</div>
            <div class="rule-content">
              <h3>遵守交通信号</h3>
              <p>严格遵守红绿灯、交通标志和交警指挥，与机动车一样遵守交通规则。</p>
            </div>
          </div>
          
          <div class="rule-item">
            <div class="rule-number">02</div>
            <div class="rule-content">
              <h3>保持安全距离</h3>
              <p>与前车保持足够的安全距离，预留充足的制动空间，避免急刹车。</p>
            </div>
          </div>
          
          <div class="rule-item">
            <div class="rule-number">03</div>
            <div class="rule-content">
              <h3>正确使用车道</h3>
              <p>在非机动车道内骑行，没有非机动车道时靠右侧骑行，不占用机动车道。</p>
            </div>
          </div>
          
          <div class="rule-item">
            <div class="rule-number">04</div>
            <div class="rule-content">
              <h3>明确转向信号</h3>
              <p>转弯或变道前提前打手势或使用转向灯，确保其他道路使用者能够预判您的行动。</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 骑行姿势指导 -->
      <section class="safety-section">
        <h2 class="section-title">
          <i class="fas fa-user-check"></i>
          正确骑行姿势
        </h2>
        <div class="posture-guide">
          <div class="posture-item">
            <div class="posture-image">
              <i class="fas fa-user-circle"></i>
            </div>
            <div class="posture-content">
              <h3>头部姿势</h3>
              <p>保持头部自然抬起，目视前方，避免长时间低头。颈部放松，不要过度紧张。</p>
            </div>
          </div>
          
          <div class="posture-item">
            <div class="posture-image">
              <i class="fas fa-hand-paper"></i>
            </div>
            <div class="posture-content">
              <h3>手部握持</h3>
              <p>双手轻握车把，手臂微弯，肩膀放松。避免死握车把，保持灵活性。</p>
            </div>
          </div>
          
          <div class="posture-item">
            <div class="posture-image">
              <i class="fas fa-chair"></i>
            </div>
            <div class="posture-content">
              <h3>坐姿调整</h3>
              <p>座椅高度适中，腿部伸展自然。上身略微前倾，保持脊柱自然弯曲。</p>
            </div>
          </div>
          
          <div class="posture-item">
            <div class="posture-image">
              <i class="fas fa-shoe-prints"></i>
            </div>
            <div class="posture-content">
              <h3>脚部位置</h3>
              <p>脚掌前部踩踏板，保持膝盖指向前方。踩踏时用力均匀，避免内外八字。</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 应急处理 -->
      <section class="safety-section">
        <h2 class="section-title">
          <i class="fas fa-first-aid"></i>
          应急处理指南
        </h2>
        <div class="emergency-grid">
          <div class="emergency-card">
            <div class="emergency-icon">
              <i class="fas fa-tools"></i>
            </div>
            <h3>设备故障</h3>
            <div class="emergency-steps">
              <div class="step">1. 立即停车检查</div>
              <div class="step">2. 移至安全区域</div>
              <div class="step">3. 使用随身工具修理</div>
              <div class="step">4. 无法修理时求助</div>
            </div>
          </div>
          
          <div class="emergency-card">
            <div class="emergency-icon">
              <i class="fas fa-cloud-rain"></i>
            </div>
            <h3>恶劣天气</h3>
            <div class="emergency-steps">
              <div class="step">1. 降低骑行速度</div>
              <div class="step">2. 增加安全距离</div>
              <div class="step">3. 使用防滑轮胎</div>
              <div class="step">4. 必要时停止骑行</div>
            </div>
          </div>
          
          <div class="emergency-card">
            <div class="emergency-icon">
              <i class="fas fa-ambulance"></i>
            </div>
            <h3>意外伤害</h3>
            <div class="emergency-steps">
              <div class="step">1. 评估伤情严重程度</div>
              <div class="step">2. 进行基础急救处理</div>
              <div class="step">3. 及时联系急救服务</div>
              <div class="step">4. 等待专业救援</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 安全检查清单 -->
      <section class="safety-section">
        <h2 class="section-title">
          <i class="fas fa-clipboard-check"></i>
          出行前安全检查
        </h2>
        <div class="checklist-container">
          <div class="checklist-category">
            <h3>车辆检查</h3>
            <div class="checklist-items">
              <label class="checklist-item">
                <input type="checkbox">
                <span class="checkmark"></span>
                轮胎气压充足，无破损
              </label>
              <label class="checklist-item">
                <input type="checkbox">
                <span class="checkmark"></span>
                刹车系统正常工作
              </label>
              <label class="checklist-item">
                <input type="checkbox">
                <span class="checkmark"></span>
                链条润滑良好
              </label>
              <label class="checklist-item">
                <input type="checkbox">
                <span class="checkmark"></span>
                车灯照明功能正常
              </label>
            </div>
          </div>
          
          <div class="checklist-category">
            <h3>个人装备</h3>
            <div class="checklist-items">
              <label class="checklist-item">
                <input type="checkbox">
                <span class="checkmark"></span>
                头盔佩戴正确
              </label>
              <label class="checklist-item">
                <input type="checkbox">
                <span class="checkmark"></span>
                穿着合适骑行服装
              </label>
              <label class="checklist-item">
                <input type="checkbox">
                <span class="checkmark"></span>
                携带必要工具
              </label>
              <label class="checklist-item">
                <input type="checkbox">
                <span class="checkmark"></span>
                手机电量充足
              </label>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  // 页面加载完成后的初始化
  console.log('安全骑行指南页面已加载')
})
</script>

<style scoped>
.safety-guide {
  min-height: 100vh;
  background: linear-gradient(135deg, #E8F5E8 0%, #F1F8E9 100%);
}

.safety-hero {
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  color: white;
  padding: 80px 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.safety-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
  animation: float 20s infinite linear;
}

@keyframes float {
  0% { transform: translateY(0px); }
  100% { transform: translateY(-100px); }
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 20px;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.9;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
}

.hero-stats .stat-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
  font-weight: 600;
}

.hero-stats .stat-item i {
  font-size: 1.5rem;
}

.safety-section {
  margin: 60px 0;
}

.section-title {
  font-size: 2.5rem;
  color: #2E7D32;
  text-align: center;
  margin-bottom: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.section-title i {
  color: #4CAF50;
}

.safety-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.safety-card {
  background: white;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(76, 175, 80, 0.1);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.safety-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(76, 175, 80, 0.2);
  border-color: #4CAF50;
}

.card-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
  font-size: 2rem;
}

.safety-card h3 {
  font-size: 1.5rem;
  color: #2E7D32;
  text-align: center;
  margin-bottom: 15px;
}

.safety-card p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.safety-card ul {
  list-style: none;
  padding: 0;
}

.safety-card li {
  padding: 8px 0;
  color: #555;
  position: relative;
  padding-left: 25px;
}

.safety-card li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #4CAF50;
  font-weight: bold;
}

.rules-container {
  max-width: 800px;
  margin: 0 auto;
}

.rule-item {
  display: flex;
  align-items: flex-start;
  gap: 30px;
  margin-bottom: 40px;
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(76, 175, 80, 0.1);
}

.rule-number {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  flex-shrink: 0;
}

.rule-content h3 {
  color: #2E7D32;
  margin-bottom: 10px;
  font-size: 1.3rem;
}

.rule-content p {
  color: #666;
  line-height: 1.6;
}

.posture-guide {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.posture-item {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(76, 175, 80, 0.1);
  text-align: center;
  transition: all 0.3s ease;
}

.posture-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(76, 175, 80, 0.2);
}

.posture-image {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #81C784, #A5D6A7);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
  font-size: 2rem;
}

.posture-content h3 {
  color: #2E7D32;
  margin-bottom: 15px;
  font-size: 1.3rem;
}

.posture-content p {
  color: #666;
  line-height: 1.6;
}

.emergency-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.emergency-card {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(255, 87, 34, 0.1);
  text-align: center;
  border-left: 5px solid #FF5722;
}

.emergency-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #FF5722, #FF7043);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
  font-size: 2rem;
}

.emergency-card h3 {
  color: #D84315;
  margin-bottom: 20px;
  font-size: 1.3rem;
}

.emergency-steps {
  text-align: left;
}

.step {
  padding: 10px 0;
  color: #666;
  border-bottom: 1px solid #eee;
  position: relative;
  padding-left: 30px;
}

.step:last-child {
  border-bottom: none;
}

.step::before {
  content: attr(data-step);
  position: absolute;
  left: 0;
  color: #FF5722;
  font-weight: bold;
}

.checklist-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 40px;
}

.checklist-category {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(76, 175, 80, 0.1);
}

.checklist-category h3 {
  color: #2E7D32;
  margin-bottom: 25px;
  font-size: 1.5rem;
  text-align: center;
  padding-bottom: 15px;
  border-bottom: 2px solid #E8F5E8;
}

.checklist-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.checklist-item {
  display: flex;
  align-items: center;
  gap: 15px;
  cursor: pointer;
  padding: 15px;
  border-radius: 10px;
  transition: all 0.3s ease;
  position: relative;
}

.checklist-item:hover {
  background: #F1F8E9;
}

.checklist-item input[type="checkbox"] {
  display: none;
}

.checkmark {
  width: 24px;
  height: 24px;
  border: 2px solid #4CAF50;
  border-radius: 4px;
  position: relative;
  transition: all 0.3s ease;
}

.checklist-item input[type="checkbox"]:checked + .checkmark {
  background: #4CAF50;
}

.checklist-item input[type="checkbox"]:checked + .checkmark::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-weight: bold;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .section-title {
    font-size: 2rem;
    flex-direction: column;
    gap: 10px;
  }
  
  .hero-stats {
    gap: 20px;
  }
  
  .rule-item {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }
  
  .checklist-container {
    grid-template-columns: 1fr;
  }
}
</style>