<template>
  <section class="hero">
    <div class="hero-content">
      <h2>探索城市周边最美骑行路线</h2>
      <p>精选三条风景各异的骑行路线，带您体验不一样的城市风光，无论您是初学者还是资深骑行爱好者，都能找到适合自己的路线</p>
      <a href="#routes" class="cta-button">查看路线</a>
    </div>
  </section>

  <main class="container">
    <section id="routes">
      <h2 class="section-title">精选骑行路线</h2>
      
      <div class="route-container">
        <!-- 路线1卡片 -->
        <div class="route-card">
          <a href="#route-detail" class="route-link">
            <div class="route-image">
              <img src="/source/湖滨休闲道.jpg" alt="湖滨休闲道景色" @load="imageLoaded($event)">
            </div>
          </a>
          <div class="route-content">
            <span class="difficulty easy">初级</span>
            <h3><a href="#route-detail" class="text-link">湖滨休闲道</a></h3>
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
            
            <a href="route1.html" class="btn btn-full">查看详情</a>
          </div>
        </div>
        
        <!-- 路线2卡片 -->
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
            
            <a href="route2.html" class="btn btn-full">查看详情</a>
          </div>
        </div>
        
        <!-- 路线3卡片 -->
        <div class="route-card">
          <a href="shiquwenhua.html" class="route-link">
            <div class="route-image">
              <img src="/source/海岸风景道.jpg" alt="海岸风景道景色" @load="imageLoaded($event)">
            </div>
          </a>
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
            
            <a href="route3.html" class="btn btn-full">查看详情</a>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
const imageLoaded = (event) => {
  event.target.parentElement.classList.add('loaded');
};
</script>

<style scoped>
/* 首页特定样式 */
.hero {
  background: linear-gradient(rgba(255, 193, 7, 0.8), rgba(230, 81, 0, 0.6)), 
              url('/source/1.jpg') center/cover fixed;
  color: #FFF8E1; /* 淡黄色文字 */
  padding: 160px 20px;
  text-align: center;
  position: relative;
  overflow: hidden;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3); /* 文字阴影增强可读性 */
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.hero::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, 
      rgba(255, 152, 0, 0.7), /* 橙色 */
      rgba(230, 81, 0, 0.3), /* 深橙色 */
      rgba(255, 193, 7, 0.5)); /* 金色 */
  animation: gradientShift 15s ease infinite;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.hero h2 {
  font-size: 2.8rem;
  margin-bottom: 20px;
}

/* 路线卡片样式 */
.route-container {
  display: grid;
  gap: 30px;
  margin-top: 40px;
}

.section-title {
  text-align: center;
  margin-bottom: 30px;
  color: #5D4037;
}

/* 路线详情页样式 */
.route-detail-container {
  margin-top: 50px;
}

.map-container {
  height: 500px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.map-controls {
  background: white;
  padding: 25px;
  border-radius: 12px;
  margin-top: 25px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.route-image {
  position: relative;
  height: 220px;
  background: #f0f3f5;
  overflow: hidden;
}

.route-image::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 40px;
  height: 40px;
  border: 3px solid #FFE0B2; /* 淡橙色边框 */
  border-top-color: #FF9800; /* 橙色顶部边框 */
  border-radius: 50%;
  animation: spin 1s linear infinite;
  transform: translate(-50%, -50%);
}

.route-image.loaded::before {
  display: none;
}

.route-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease, opacity 0.3s ease;
  opacity: 0;
}

.route-image.loaded img {
  opacity: 1;
}

@keyframes spin {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}
</style>