<template>
  <div class="maintenance-guide">
    <!-- 页面头部 -->
    <section class="hero maintenance-hero">
      <div class="hero-content">
        <h1>设备保养技巧</h1>
        <p>延长装备使用寿命的维护秘诀，让您的爱车始终保持最佳状态</p>
        <div class="hero-stats">
          <div class="stat-item">
            <i class="fas fa-tools"></i>
            <span>专业维护</span>
          </div>
          <div class="stat-item">
            <i class="fas fa-clock"></i>
            <span>延长寿命</span>
          </div>
          <div class="stat-item">
            <i class="fas fa-money-bill-wave"></i>
            <span>节省成本</span>
          </div>
        </div>
      </div>
    </section>

    <main class="container">
      <!-- 日常保养 -->
      <section class="maintenance-section">
        <h2 class="section-title">
          <i class="fas fa-calendar-day"></i>
          日常保养指南
        </h2>
        <div class="maintenance-grid">
          <div class="maintenance-card">
            <div class="card-icon">
              <i class="fas fa-tint"></i>
            </div>
            <h3>清洁保养</h3>
            <p>定期清洁是保持自行车良好状态的基础，正确的清洁方法能有效延长各部件寿命。</p>
            <div class="maintenance-steps">
              <div class="step">
                <span class="step-number">1</span>
                <div class="step-content">
                  <h4>准备清洁用品</h4>
                  <p>准备软毛刷、清洁剂、抹布和润滑油</p>
                </div>
              </div>
              <div class="step">
                <span class="step-number">2</span>
                <div class="step-content">
                  <h4>冲洗车身</h4>
                  <p>用清水冲洗车身，去除表面泥土和灰尘</p>
                </div>
              </div>
              <div class="step">
                <span class="step-number">3</span>
                <div class="step-content">
                  <h4>深度清洁</h4>
                  <p>使用专用清洁剂和软毛刷清洁链条和齿轮</p>
                </div>
              </div>
              <div class="step">
                <span class="step-number">4</span>
                <div class="step-content">
                  <h4>干燥润滑</h4>
                  <p>彻底干燥后对链条等活动部件进行润滑</p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="maintenance-card">
            <div class="card-icon">
              <i class="fas fa-search"></i>
            </div>
            <h3>定期检查</h3>
            <p>定期检查各个部件的状态，及时发现问题并处理，避免小问题变成大故障。</p>
            <div class="check-list">
              <div class="check-item">
                <i class="fas fa-check-circle"></i>
                <span>轮胎气压和磨损情况</span>
              </div>
              <div class="check-item">
                <i class="fas fa-check-circle"></i>
                <span>刹车片厚度和制动效果</span>
              </div>
              <div class="check-item">
                <i class="fas fa-check-circle"></i>
                <span>链条张力和润滑状态</span>
              </div>
              <div class="check-item">
                <i class="fas fa-check-circle"></i>
                <span>螺丝紧固程度</span>
              </div>
              <div class="check-item">
                <i class="fas fa-check-circle"></i>
                <span>变速器调节精度</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 部件维护 -->
      <section class="maintenance-section">
        <h2 class="section-title">
          <i class="fas fa-cogs"></i>
          核心部件维护
        </h2>
        <div class="parts-container">
          <div class="part-card">
            <div class="part-header">
              <div class="part-icon">
                <i class="fas fa-link"></i>
              </div>
              <h3>链条系统</h3>
            </div>
            <div class="part-content">
              <div class="maintenance-frequency">
                <span class="frequency-label">保养频率：</span>
                <span class="frequency-value">每200公里</span>
              </div>
              <div class="maintenance-tips">
                <h4>保养要点：</h4>
                <ul>
                  <li>使用专用链条清洁剂去除污垢</li>
                  <li>清洁后涂抹适量链条润滑油</li>
                  <li>检查链条磨损程度，及时更换</li>
                  <li>保持链条适当张力</li>
                </ul>
              </div>
              <div class="warning-box">
                <i class="fas fa-exclamation-triangle"></i>
                <p>注意：过度润滑会吸附更多灰尘，适量即可</p>
              </div>
            </div>
          </div>
          
          <div class="part-card">
            <div class="part-header">
              <div class="part-icon">
                <i class="fas fa-stop-circle"></i>
              </div>
              <h3>刹车系统</h3>
            </div>
            <div class="part-content">
              <div class="maintenance-frequency">
                <span class="frequency-label">保养频率：</span>
                <span class="frequency-value">每月检查</span>
              </div>
              <div class="maintenance-tips">
                <h4>保养要点：</h4>
                <ul>
                  <li>检查刹车片磨损情况</li>
                  <li>调整刹车线张力</li>
                  <li>清洁刹车盘表面</li>
                  <li>确保刹车手感正常</li>
                </ul>
              </div>
              <div class="warning-box">
                <i class="fas fa-exclamation-triangle"></i>
                <p>警告：刹车系统关乎安全，发现异常立即处理</p>
              </div>
            </div>
          </div>
          
          <div class="part-card">
            <div class="part-header">
              <div class="part-icon">
                <i class="fas fa-circle"></i>
              </div>
              <h3>轮胎轮圈</h3>
            </div>
            <div class="part-content">
              <div class="maintenance-frequency">
                <span class="frequency-label">保养频率：</span>
                <span class="frequency-value">每周检查</span>
              </div>
              <div class="maintenance-tips">
                <h4>保养要点：</h4>
                <ul>
                  <li>保持适当的轮胎气压</li>
                  <li>检查轮胎花纹磨损</li>
                  <li>清除轮胎上的异物</li>
                  <li>检查轮圈是否变形</li>
                </ul>
              </div>
              <div class="tip-box">
                <i class="fas fa-lightbulb"></i>
                <p>小贴士：正确的气压能提升骑行效率并减少爆胎风险</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 季节性保养 -->
      <section class="maintenance-section">
        <h2 class="section-title">
          <i class="fas fa-calendar-alt"></i>
          季节性保养计划
        </h2>
        <div class="seasonal-maintenance">
          <div class="season-card spring">
            <div class="season-header">
              <i class="fas fa-seedling"></i>
              <h3>春季保养</h3>
            </div>
            <div class="season-content">
              <h4>重点任务：</h4>
              <ul>
                <li>全面清洁和检查</li>
                <li>更换磨损的部件</li>
                <li>调整变速和刹车系统</li>
                <li>检查轮胎状况</li>
              </ul>
              <div class="season-tip">
                <strong>春季提醒：</strong>经过冬季存放，需要全面检查各部件状态
              </div>
            </div>
          </div>
          
          <div class="season-card summer">
            <div class="season-header">
              <i class="fas fa-sun"></i>
              <h3>夏季保养</h3>
            </div>
            <div class="season-content">
              <h4>重点任务：</h4>
              <ul>
                <li>增加清洁频率</li>
                <li>检查轮胎气压</li>
                <li>注意链条润滑</li>
                <li>防止过度暴晒</li>
              </ul>
              <div class="season-tip">
                <strong>夏季提醒：</strong>高温和频繁使用需要更勤的保养
              </div>
            </div>
          </div>
          
          <div class="season-card autumn">
            <div class="season-header">
              <i class="fas fa-leaf"></i>
              <h3>秋季保养</h3>
            </div>
            <div class="season-content">
              <h4>重点任务：</h4>
              <ul>
                <li>清除落叶和杂物</li>
                <li>检查刹车性能</li>
                <li>准备防雨措施</li>
                <li>增强照明设备</li>
              </ul>
              <div class="season-tip">
                <strong>秋季提醒：</strong>多雨季节要特别注意防锈和防水
              </div>
            </div>
          </div>
          
          <div class="season-card winter">
            <div class="season-header">
              <i class="fas fa-snowflake"></i>
              <h3>冬季保养</h3>
            </div>
            <div class="season-content">
              <h4>重点任务：</h4>
              <ul>
                <li>彻底清洁和干燥</li>
                <li>涂抹防锈剂</li>
                <li>适当放松线缆</li>
                <li>选择合适存放环境</li>
              </ul>
              <div class="season-tip">
                <strong>冬季提醒：</strong>长期存放需要做好防潮防锈工作
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 工具推荐 -->
      <section class="maintenance-section">
        <h2 class="section-title">
          <i class="fas fa-toolbox"></i>
          必备工具推荐
        </h2>
        <div class="tools-grid">
          <div class="tool-category">
            <h3>基础工具</h3>
            <div class="tool-list">
              <div class="tool-item">
                <div class="tool-icon">
                  <i class="fas fa-wrench"></i>
                </div>
                <div class="tool-info">
                  <h4>多功能扳手</h4>
                  <p>调节螺丝和螺母的基本工具</p>
                  <span class="price-range">¥30-80</span>
                </div>
              </div>
              <div class="tool-item">
                <div class="tool-icon">
                  <i class="fas fa-pump"></i>
                </div>
                <div class="tool-info">
                  <h4>便携打气筒</h4>
                  <p>维持轮胎适当气压</p>
                  <span class="price-range">¥50-150</span>
                </div>
              </div>
              <div class="tool-item">
                <div class="tool-icon">
                  <i class="fas fa-cut"></i>
                </div>
                <div class="tool-info">
                  <h4>链条工具</h4>
                  <p>拆装和维护链条专用</p>
                  <span class="price-range">¥20-60</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="tool-category">
            <h3>清洁用品</h3>
            <div class="tool-list">
              <div class="tool-item">
                <div class="tool-icon">
                  <i class="fas fa-spray-can"></i>
                </div>
                <div class="tool-info">
                  <h4>链条清洁剂</h4>
                  <p>专业去污，保护金属表面</p>
                  <span class="price-range">¥25-50</span>
                </div>
              </div>
              <div class="tool-item">
                <div class="tool-icon">
                  <i class="fas fa-oil-can"></i>
                </div>
                <div class="tool-info">
                  <h4>链条润滑油</h4>
                  <p>减少磨损，提升传动效率</p>
                  <span class="price-range">¥30-80</span>
                </div>
              </div>
              <div class="tool-item">
                <div class="tool-icon">
                  <i class="fas fa-brush"></i>
                </div>
                <div class="tool-info">
                  <h4>清洁刷套装</h4>
                  <p>不同硬度，适用各种部件</p>
                  <span class="price-range">¥15-40</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 故障诊断 -->
      <section class="maintenance-section">
        <h2 class="section-title">
          <i class="fas fa-stethoscope"></i>
          常见故障诊断
        </h2>
        <div class="troubleshooting">
          <div class="problem-card">
            <div class="problem-header">
              <i class="fas fa-exclamation-circle"></i>
              <h3>链条异响</h3>
            </div>
            <div class="problem-content">
              <div class="symptoms">
                <h4>症状表现：</h4>
                <p>骑行时链条发出咔咔声或摩擦声</p>
              </div>
              <div class="causes">
                <h4>可能原因：</h4>
                <ul>
                  <li>链条缺乏润滑</li>
                  <li>链条过度磨损</li>
                  <li>变速器调节不当</li>
                  <li>链条张力不合适</li>
                </ul>
              </div>
              <div class="solutions">
                <h4>解决方案：</h4>
                <ol>
                  <li>清洁并润滑链条</li>
                  <li>调整变速器</li>
                  <li>检查链条磨损程度</li>
                  <li>必要时更换链条</li>
                </ol>
              </div>
            </div>
          </div>
          
          <div class="problem-card">
            <div class="problem-header">
              <i class="fas fa-exclamation-circle"></i>
              <h3>刹车失灵</h3>
            </div>
            <div class="problem-content">
              <div class="symptoms">
                <h4>症状表现：</h4>
                <p>刹车手感软弱或制动距离过长</p>
              </div>
              <div class="causes">
                <h4>可能原因：</h4>
                <ul>
                  <li>刹车片磨损严重</li>
                  <li>刹车线松弛</li>
                  <li>刹车盘污染</li>
                  <li>刹车系统进水</li>
                </ul>
              </div>
              <div class="solutions">
                <h4>解决方案：</h4>
                <ol>
                  <li>检查刹车片厚度</li>
                  <li>调整刹车线张力</li>
                  <li>清洁刹车盘表面</li>
                  <li>更换磨损的刹车片</li>
                </ol>
              </div>
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
  console.log('设备保养技巧页面已加载')
})
</script>

<style scoped>
.maintenance-guide {
  min-height: 100vh;
  background: linear-gradient(135deg, #E3F2FD 0%, #F1F8FF 100%);
}

.maintenance-hero {
  background: linear-gradient(135deg, #2196F3 0%, #42A5F5 100%);
  color: white;
  padding: 80px 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.maintenance-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><polygon points="50,10 60,35 85,35 65,55 75,80 50,65 25,80 35,55 15,35 40,35" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
  animation: rotate 30s infinite linear;
}

@keyframes rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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

.maintenance-section {
  margin: 60px 0;
}

.section-title {
  font-size: 2.5rem;
  color: #1565C0;
  text-align: center;
  margin-bottom: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.section-title i {
  color: #2196F3;
}

.maintenance-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 40px;
}

.maintenance-card {
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(33, 150, 243, 0.1);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.maintenance-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(33, 150, 243, 0.2);
  border-color: #2196F3;
}

.card-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #2196F3, #42A5F5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 25px;
  color: white;
  font-size: 2rem;
}

.maintenance-card h3 {
  font-size: 1.8rem;
  color: #1565C0;
  text-align: center;
  margin-bottom: 20px;
}

.maintenance-card p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 30px;
  text-align: center;
}

.maintenance-steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  padding: 20px;
  background: #F8FBFF;
  border-radius: 12px;
  border-left: 4px solid #2196F3;
}

.step-number {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #2196F3, #42A5F5);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.step-content h4 {
  color: #1565C0;
  margin-bottom: 8px;
  font-size: 1.1rem;
}

.step-content p {
  color: #666;
  margin: 0;
  text-align: left;
}

.check-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.check-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: #F8FBFF;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.check-item:hover {
  background: #E3F2FD;
  transform: translateX(5px);
}

.check-item i {
  color: #2196F3;
  font-size: 1.2rem;
}

.check-item span {
  color: #555;
  font-weight: 500;
}

.parts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
}

.part-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(33, 150, 243, 0.1);
  transition: all 0.3s ease;
}

.part-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(33, 150, 243, 0.2);
}

.part-header {
  background: linear-gradient(135deg, #2196F3, #42A5F5);
  color: white;
  padding: 25px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.part-icon {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.part-header h3 {
  font-size: 1.5rem;
  margin: 0;
}

.part-content {
  padding: 30px;
}

.maintenance-frequency {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 25px;
  padding: 15px;
  background: #E3F2FD;
  border-radius: 10px;
}

.frequency-label {
  color: #1565C0;
  font-weight: 600;
}

.frequency-value {
  color: #2196F3;
  font-weight: bold;
  font-size: 1.1rem;
}

.maintenance-tips h4 {
  color: #1565C0;
  margin-bottom: 15px;
  font-size: 1.2rem;
}

.maintenance-tips ul {
  list-style: none;
  padding: 0;
}

.maintenance-tips li {
  padding: 8px 0;
  color: #555;
  position: relative;
  padding-left: 25px;
}

.maintenance-tips li::before {
  content: '▶';
  position: absolute;
  left: 0;
  color: #2196F3;
  font-size: 0.8rem;
}

.warning-box, .tip-box {
  margin-top: 20px;
  padding: 15px;
  border-radius: 10px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.warning-box {
  background: #FFF3E0;
  border-left: 4px solid #FF9800;
}

.warning-box i {
  color: #FF9800;
  margin-top: 2px;
}

.warning-box p {
  color: #E65100;
  margin: 0;
  font-weight: 500;
}

.tip-box {
  background: #F1F8E9;
  border-left: 4px solid #4CAF50;
}

.tip-box i {
  color: #4CAF50;
  margin-top: 2px;
}

.tip-box p {
  color: #2E7D32;
  margin: 0;
  font-weight: 500;
}

.seasonal-maintenance {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}

.season-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.season-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.season-card.spring .season-header {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
}

.season-card.summer .season-header {
  background: linear-gradient(135deg, #FF9800, #FFB74D);
}

.season-card.autumn .season-header {
  background: linear-gradient(135deg, #FF5722, #FF7043);
}

.season-card.winter .season-header {
  background: linear-gradient(135deg, #607D8B, #78909C);
}

.season-header {
  color: white;
  padding: 25px;
  text-align: center;
}

.season-header i {
  font-size: 2.5rem;
  margin-bottom: 15px;
  display: block;
}

.season-header h3 {
  font-size: 1.5rem;
  margin: 0;
}

.season-content {
  padding: 30px;
}

.season-content h4 {
  color: #1565C0;
  margin-bottom: 15px;
}

.season-content ul {
  list-style: none;
  padding: 0;
  margin-bottom: 20px;
}

.season-content li {
  padding: 8px 0;
  color: #555;
  position: relative;
  padding-left: 20px;
}

.season-content li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #2196F3;
  font-weight: bold;
}

.season-tip {
  background: #E3F2FD;
  padding: 15px;
  border-radius: 10px;
  border-left: 4px solid #2196F3;
}

.season-tip strong {
  color: #1565C0;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 40px;
}

.tool-category {
  background: white;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(33, 150, 243, 0.1);
}

.tool-category h3 {
  color: #1565C0;
  font-size: 1.5rem;
  margin-bottom: 25px;
  text-align: center;
  padding-bottom: 15px;
  border-bottom: 2px solid #E3F2FD;
}

.tool-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.tool-item {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: #F8FBFF;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.tool-item:hover {
  background: #E3F2FD;
  transform: translateX(5px);
}

.tool-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #2196F3, #42A5F5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.tool-info h4 {
  color: #1565C0;
  margin-bottom: 5px;
  font-size: 1.1rem;
}

.tool-info p {
  color: #666;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.price-range {
  color: #2196F3;
  font-weight: bold;
  font-size: 0.9rem;
}

.troubleshooting {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 30px;
}

.problem-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(244, 67, 54, 0.1);
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.problem-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(244, 67, 54, 0.2);
  border-color: #F44336;
}

.problem-header {
  background: linear-gradient(135deg, #F44336, #E57373);
  color: white;
  padding: 25px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.problem-header i {
  font-size: 1.5rem;
}

.problem-header h3 {
  font-size: 1.3rem;
  margin: 0;
}

.problem-content {
  padding: 30px;
}

.symptoms, .causes, .solutions {
  margin-bottom: 25px;
}

.symptoms h4, .causes h4, .solutions h4 {
  color: #D32F2F;
  margin-bottom: 10px;
  font-size: 1.1rem;
}

.symptoms p {
  color: #666;
  font-style: italic;
}

.causes ul, .solutions ol {
  padding-left: 20px;
}

.causes li, .solutions li {
  color: #555;
  margin-bottom: 8px;
  line-height: 1.5;
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
  
  .maintenance-grid {
    grid-template-columns: 1fr;
  }
  
  .parts-container {
    grid-template-columns: 1fr;
  }
  
  .tools-grid {
    grid-template-columns: 1fr;
  }
  
  .troubleshooting {
    grid-template-columns: 1fr;
  }
  
  .step {
    flex-direction: column;
    text-align: center;
  }
}
</style>