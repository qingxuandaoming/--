<template>
  <!-- Hero 区域 -->
  <section class="hero">
    <div class="hero-content">
      <h1>探索城市周边最美骑行路线</h1>
      <p>精选风景各异的骑行路线，无论初学者还是资深骑友，都能找到属于自己的风景</p>
      <div class="hero-actions">
        <a href="#routes" class="cta-button">探索路线</a>
        <router-link to="/route-planning" class="cta-button-outline">
          <i class="fas fa-route"></i> 智能规划
        </router-link>
      </div>
      <div class="hero-stats-mini">
        <span><strong>28+</strong> 精选路线</span>
        <span><strong>12,000+</strong> 活跃骑友</span>
        <span><strong>86,000km</strong> 累计骑行</span>
      </div>
    </div>
  </section>

  <!-- 精选骑行路线 -->
  <main class="container">
    <section id="routes">
      <h2 class="section-title">精选骑行路线</h2>

      <div class="route-container">
        <div class="route-card">
          <div class="route-image">
            <img src="/source/湖滨休闲道.jpg" alt="湖滨休闲道景色" @load="imageLoaded($event)">
          </div>
          <div class="route-content">
            <span class="difficulty easy">初级</span>
            <h3>湖滨休闲道</h3>
            <p>沿湖岸骑行的平缓路线，景色宜人，适合家庭和初学者的轻松骑行体验...</p>
            <div class="route-stats">
              <div class="stat-item">
                <i class="fas fa-route"></i>
                <h4>距离</h4>
                <p>12 公里</p>
              </div>
              <div class="stat-item">
                <i class="far fa-clock"></i>
                <h4>时间</h4>
                <p>1-2 小时</p>
              </div>
              <div class="stat-item">
                <i class="fas fa-mountain"></i>
                <h4>海拔</h4>
                <p>50m</p>
              </div>
            </div>
            <router-link to="/route-planning" class="btn btn-full">查看详情</router-link>
          </div>
        </div>

        <div class="route-card">
          <div class="route-image">
            <img src="/source/森林山地线.jpg" alt="森林山地线景色" @load="imageLoaded($event)">
          </div>
          <div class="route-content">
            <span class="difficulty moderate">中级</span>
            <h3>森林山地线</h3>
            <p>穿越茂密森林的山地路线，起伏多变，带来刺激的骑行体验和清新的森林空气...</p>
            <div class="route-stats">
              <div class="stat-item">
                <i class="fas fa-route"></i>
                <h4>距离</h4>
                <p>25 公里</p>
              </div>
              <div class="stat-item">
                <i class="far fa-clock"></i>
                <h4>时间</h4>
                <p>3-4 小时</p>
              </div>
              <div class="stat-item">
                <i class="fas fa-mountain"></i>
                <h4>海拔</h4>
                <p>320m</p>
              </div>
            </div>
            <router-link to="/route-planning" class="btn btn-full">查看详情</router-link>
          </div>
        </div>

        <div class="route-card">
          <div class="route-image">
            <img src="/source/海岸风景道.jpg" alt="海岸风景道景色" @load="imageLoaded($event)">
          </div>
          <div class="route-content">
            <span class="difficulty challenging">高级</span>
            <h3>海岸风景道</h3>
            <p>沿海岸线蜿蜒的挑战性路线，壮观的海洋景色与身体挑战并存，极致骑行体验...</p>
            <div class="route-stats">
              <div class="stat-item">
                <i class="fas fa-route"></i>
                <h4>距离</h4>
                <p>40 公里</p>
              </div>
              <div class="stat-item">
                <i class="far fa-clock"></i>
                <h4>时间</h4>
                <p>5-6 小时</p>
              </div>
              <div class="stat-item">
                <i class="fas fa-mountain"></i>
                <h4>海拔</h4>
                <p>580m</p>
              </div>
            </div>
            <router-link to="/route-planning" class="btn btn-full">查看详情</router-link>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- 平台数据统计 -->
  <section class="stats-showcase">
    <div class="container">
      <h2 class="section-title">骑行者社区的数据</h2>
      <div class="stats-grid">
        <div class="stat-card" v-for="(item, index) in statsData" :key="index">
          <div class="stat-icon"><i :class="'fas ' + item.icon"></i></div>
          <div class="stat-number">{{ item.number }}</div>
          <div class="stat-unit">{{ item.unit }}</div>
          <div class="stat-label">{{ item.label }}</div>
        </div>
      </div>
    </div>
  </section>

  <!-- 特色功能探索 -->
  <section class="features-explore">
    <div class="container">
      <h2 class="section-title">特色功能探索</h2>
      <p class="section-subtitle">不止于路线，我们为你提供全方位的骑行体验</p>

      <div class="features-grid">
        <router-link to="/intangible-heritage-map" class="feature-card">
          <div class="feature-icon heritage">
            <i class="fas fa-landmark"></i>
          </div>
          <h3>非遗骑行地图</h3>
          <p>穿越千年文脉，用车轮丈量非遗之美。精选10个非遗乡村骑行线路。</p>
          <span class="feature-link">探索非遗路线 <i class="fas fa-arrow-right"></i></span>
        </router-link>

        <router-link to="/vr" class="feature-card">
          <div class="feature-icon vr">
            <i class="fas fa-vr-cardboard"></i>
          </div>
          <h3>VR灵境</h3>
          <p>足不出户，身临其境。360°沉浸式预览沿途风景，提前规划你的骑行。</p>
          <span class="feature-link">进入VR体验 <i class="fas fa-arrow-right"></i></span>
        </router-link>

        <router-link to="/equipment" class="feature-card">
          <div class="feature-icon equipment">
            <i class="fas fa-bicycle"></i>
          </div>
          <h3>装备推荐</h3>
          <p>基于大数据分析的骑行装备选购指南，从入门到专业，一站配齐。</p>
          <span class="feature-link">查看装备 <i class="fas fa-arrow-right"></i></span>
        </router-link>

        <router-link to="/route-planning" class="feature-card">
          <div class="feature-icon planning">
            <i class="fas fa-route"></i>
          </div>
          <h3>智能路线规划</h3>
          <p>基于高德地图API，输入起点终点，自动生成最优骑行路线。</p>
          <span class="feature-link">开始规划 <i class="fas fa-arrow-right"></i></span>
        </router-link>
      </div>
    </div>
  </section>

  <!-- 为什么选择我们 -->
  <section class="why-choose-us">
    <div class="container">
      <div class="value-content">
        <div class="value-text">
          <h2 class="section-title left">为什么选择我们</h2>
          <p class="value-desc">我们不仅提供路线，更致力于打造完整的骑行生态系统</p>

          <div class="value-list">
            <div class="value-item">
              <div class="value-icon"><i class="fas fa-check-circle"></i></div>
              <div>
                <h4>精选实测路线</h4>
                <p>每条路线均经过实地骑行验证，附详细路况、海拔、设施信息</p>
              </div>
            </div>
            <div class="value-item">
              <div class="value-icon"><i class="fas fa-check-circle"></i></div>
              <div>
                <h4>智能路线规划</h4>
                <p>接入高德地图API，支持任意两点间的骑行路线规划与导航</p>
              </div>
            </div>
            <div class="value-item">
              <div class="value-icon"><i class="fas fa-check-circle"></i></div>
              <div>
                <h4>文化+骑行融合</h4>
                <p>独创非遗骑行地图，让骑行不仅是运动，更是一场文化之旅</p>
              </div>
            </div>
            <div class="value-item">
              <div class="value-icon"><i class="fas fa-check-circle"></i></div>
              <div>
                <h4>装备数据支持</h4>
                <p>基于后端数据分析的装备推荐与价格趋势，让选购更明智</p>
              </div>
            </div>
          </div>
        </div>

        <div class="value-visual">
          <img src="/source/森林山地线.jpg" alt="骑行体验">
          <div class="value-badge">
            <i class="fas fa-award"></i>
            <span>最佳骑行平台</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 底部 CTA -->
  <section class="bottom-cta">
    <div class="container">
      <h2>准备好出发了吗？</h2>
      <p>加入我们的骑行社区，发现更多精彩路线与志同道合的骑友</p>
      <div class="cta-actions">
        <router-link to="/register" class="cta-button">免费注册</router-link>
        <router-link to="/route-planning" class="cta-button-outline">
          <i class="fas fa-route"></i> 先试规划
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const imageLoaded = (event) => {
  event.target.parentElement.classList.add('loaded');
};

const statsData = ref([
  { icon: 'fa-road', number: '86', unit: '万公里', label: '累计骑行里程' },
  { icon: 'fa-map-marked-alt', number: '28', unit: '条', label: '精选骑行路线' },
  { icon: 'fa-users', number: '12,000', unit: '+', label: '活跃骑行用户' },
  { icon: 'fa-mountain', number: '158', unit: '万米', label: '累计爬升海拔' }
])
</script>

<style scoped>
/* Hero 区域 */
.hero {
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.9), rgba(230, 81, 0, 0.7)),
              url('/source/湖滨休闲道.jpg') center/cover fixed;
  color: #FFFFFF;
  padding: 120px 20px 80px;
  text-align: center;
  position: relative;
  overflow: hidden;
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg,
      rgba(255, 152, 0, 0.8),
      rgba(230, 81, 0, 0.6),
      rgba(255, 193, 7, 0.7));
  animation: gradientShift 20s ease infinite;
  z-index: 0;
}

@keyframes gradientShift {
  0%, 100% {
    background: linear-gradient(135deg,
        rgba(255, 152, 0, 0.8),
        rgba(230, 81, 0, 0.6),
        rgba(255, 193, 7, 0.7));
  }
  50% {
    background: linear-gradient(135deg,
        rgba(255, 193, 7, 0.8),
        rgba(255, 152, 0, 0.7),
        rgba(230, 81, 0, 0.6));
  }
}

.hero-content {
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
  padding: 40px 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.hero h1 {
  font-size: clamp(2.2rem, 5vw, 3.5rem);
  margin-bottom: 24px;
  font-weight: 700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  line-height: 1.2;
}

.hero p {
  font-size: clamp(1.1rem, 2.5vw, 1.3rem);
  margin-bottom: 32px;
  line-height: 1.6;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
  opacity: 0.95;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.cta-button {
  display: inline-block;
  padding: 16px 40px;
  background: linear-gradient(135deg, #FF6B35, #F7931E);
  color: white;
  text-decoration: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);
  text-transform: uppercase;
  letter-spacing: 1px;
  border: none;
  cursor: pointer;
}

.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.6);
  background: linear-gradient(135deg, #FF8A65, #FFB74D);
}

.cta-button-outline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 16px 40px;
  background: transparent;
  color: white;
  text-decoration: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  border: 2px solid rgba(255, 255, 255, 0.6);
  cursor: pointer;
}

.cta-button-outline:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: white;
  transform: translateY(-3px);
}

.hero-stats-mini {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
  font-size: 0.95rem;
  opacity: 0.9;
}

.hero-stats-mini span {
  display: flex;
  align-items: center;
  gap: 6px;
}

.hero-stats-mini strong {
  font-size: 1.4rem;
  font-weight: 700;
}

/* 主要内容区域 */
.container {
  padding: 60px 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: clamp(2rem, 4vw, 2.8rem);
  margin-bottom: 50px;
  color: #2C3E50;
  font-weight: 700;
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background: linear-gradient(135deg, #FF9800, #F57C00);
  border-radius: 2px;
}

.section-title.left {
  text-align: left;
}

.section-title.left::after {
  left: 0;
  transform: none;
}

/* 路线卡片 */
.route-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 40px;
  margin-top: 60px;
}

.route-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.4s ease;
  position: relative;
  border: 1px solid rgba(255, 152, 0, 0.1);
}

.route-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border-color: rgba(255, 152, 0, 0.3);
}

.route-image {
  position: relative;
  height: 250px;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  overflow: hidden;
}

.route-image::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 40px;
  height: 40px;
  border: 3px solid #FFE0B2;
  border-top-color: #FF9800;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  transform: translate(-50%, -50%);
  z-index: 1;
}

.route-image.loaded::before {
  display: none;
}

.route-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 0.4s ease;
  opacity: 0;
}

.route-image.loaded img {
  opacity: 1;
}

.route-card:hover .route-image img {
  transform: scale(1.05);
}

.route-content {
  padding: 30px;
}

.route-content h3 {
  font-size: 1.5rem;
  margin: 15px 0;
  color: #2C3E50;
  font-weight: 600;
}

.route-content p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 25px;
  font-size: 0.95rem;
}

.route-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin: 25px 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
}

.stat-item {
  text-align: center;
}

.stat-item i {
  font-size: 1.2rem;
  color: #FF9800;
  margin-bottom: 8px;
}

.stat-item h4 {
  font-size: 0.85rem;
  color: #666;
  margin: 5px 0;
  font-weight: 500;
}

.stat-item p {
  font-size: 1rem;
  font-weight: 600;
  color: #2C3E50;
  margin: 0;
}

.btn-full {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn-full:hover {
  background: linear-gradient(135deg, #FFB74D, #FF9800);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 152, 0, 0.4);
}

.difficulty {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 25px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 15px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.difficulty.easy {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

.difficulty.moderate {
  background: linear-gradient(135deg, #FF9800, #FFB74D);
  color: white;
  box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
}

.difficulty.challenging {
  background: linear-gradient(135deg, #F44336, #E57373);
  color: white;
  box-shadow: 0 2px 8px rgba(244, 67, 54, 0.3);
}

/* 数据统计区域 */
.stats-showcase {
  background: linear-gradient(135deg, #FFF8F0 0%, #FFF3E0 100%);
  padding: 80px 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.stat-card {
  background: white;
  border-radius: 20px;
  padding: 35px 25px;
  text-align: center;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 152, 0, 0.1);
}

.stat-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
}

.stat-card .stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  font-size: 1.5rem;
}

.stat-card .stat-number {
  font-size: 2.4rem;
  font-weight: 700;
  color: #2C3E50;
  line-height: 1.2;
}

.stat-card .stat-unit {
  font-size: 1rem;
  color: #FF9800;
  font-weight: 600;
  margin-bottom: 4px;
}

.stat-card .stat-label {
  font-size: 0.9rem;
  color: #666;
}

/* 特色功能探索 */
.features-explore {
  padding: 80px 20px;
  background: white;
}

.features-explore .section-subtitle {
  text-align: center;
  color: #666;
  font-size: 1.1rem;
  margin-top: -30px;
  margin-bottom: 50px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: white;
  border-radius: 20px;
  padding: 35px 30px;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  transition: all 0.4s ease;
  border: 1px solid rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
  border-color: rgba(255, 152, 0, 0.2);
}

.feature-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
  color: white;
  margin-bottom: 20px;
}

.feature-icon.heritage {
  background: linear-gradient(135deg, #E65100, #FF9800);
}

.feature-icon.vr {
  background: linear-gradient(135deg, #7B1FA2, #AB47BC);
}

.feature-icon.equipment {
  background: linear-gradient(135deg, #FF6F00, #FFA726);
}

.feature-icon.planning {
  background: linear-gradient(135deg, #2E7D32, #66BB6A);
}

.feature-card h3 {
  font-size: 1.3rem;
  color: #2C3E50;
  margin-bottom: 10px;
  font-weight: 600;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
  font-size: 0.95rem;
  margin-bottom: 20px;
  flex: 1;
}

.feature-link {
  color: #FF9800;
  font-weight: 600;
  font-size: 0.95rem;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
}

.feature-card:hover .feature-link {
  gap: 10px;
}

.feature-link i {
  font-size: 0.8rem;
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-link i {
  transform: translateX(4px);
}

/* 为什么选择我们 */
.why-choose-us {
  padding: 80px 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.value-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.value-desc {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 30px;
  line-height: 1.6;
}

.value-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.value-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.value-item .value-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  flex-shrink: 0;
  margin-top: 2px;
}

.value-item h4 {
  color: #2C3E50;
  font-size: 1.1rem;
  margin-bottom: 4px;
  font-weight: 600;
}

.value-item p {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
}

.value-visual {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.value-visual img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.value-badge {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  padding: 12px 20px;
  border-radius: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(255, 152, 0, 0.4);
}

/* 底部 CTA */
.bottom-cta {
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.9), rgba(230, 81, 0, 0.8));
  padding: 80px 20px;
  text-align: center;
  color: white;
}

.bottom-cta h2 {
  font-size: clamp(1.8rem, 4vw, 2.6rem);
  margin-bottom: 16px;
  font-weight: 700;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
}

.bottom-cta p {
  font-size: 1.1rem;
  opacity: 0.95;
  margin-bottom: 32px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.15);
}

.cta-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .value-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .value-visual {
    order: -1;
    max-height: 350px;
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 80px 15px 60px;
    min-height: 60vh;
  }

  .hero-content {
    padding: 30px 15px;
  }

  .hero-actions {
    flex-direction: column;
    align-items: center;
  }

  .cta-button,
  .cta-button-outline {
    width: 100%;
    max-width: 280px;
    justify-content: center;
  }

  .hero-stats-mini {
    gap: 20px;
  }

  .route-container {
    grid-template-columns: 1fr;
    gap: 30px;
    margin-top: 40px;
  }

  .route-stats {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .container {
    padding: 40px 15px;
  }

  .stats-showcase,
  .features-explore,
  .why-choose-us,
  .bottom-cta {
    padding: 50px 15px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .hero {
    min-height: 50vh;
    padding: 60px 10px 40px;
  }

  .route-content {
    padding: 20px;
  }

  .route-image {
    height: 200px;
  }
}

@keyframes spin {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}
</style>
