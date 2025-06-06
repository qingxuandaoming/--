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
              <img src="/source/市区文化线.jpg" alt="市区文化线景色" @load="imageLoaded($event)">
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

  <!-- 路线详情页 -->
  <main class="route-detail-container container">
    <section class="map-section">
      <!-- 优化后的地图容器 - 支持高德地图API -->
      <div id="container" class="map-container">
        <!-- 地图将通过高德地图API加载 -->
        <!-- 需接入高德地图API -->
      </div>
      
      <!-- 地图控制面板 - 支持起点终点选择 -->
      <div class="map-controls">
        <h3><i class="fas fa-map-marked-alt"></i> 路线规划</h3>
        
        <div class="control-group">
          <label for="startPoint"><i class="fas fa-play"></i> 起点</label>
          <input type="text" id="startPoint" placeholder="输入或点击地图选择起点">
        </div>
        
        <div class="control-group">
          <label for="endPoint"><i class="fas fa-flag-checkered"></i> 终点</label>
          <input type="text" id="endPoint" placeholder="输入或点击地图选择终点">
        </div>
        
        <button class="btn btn-full" id="calculateRoute">
          <i class="fas fa-route"></i> 规划路线
        </button>
      </div>
    </section>
    
    <section class="route-info-section">
      <div class="info-main">
        <div class="route-header">
          <span class="difficulty easy">初级</span>
          <h1>湖滨休闲道</h1>
          
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
            <div class="stat-item">
              <i class="fas fa-road"></i>
              <h4>路面</h4>
              <p>柏油路</p>
            </div>
          </div>
        </div>
        
        <div class="route-description">
          <!-- 文字内容来源: {{CONTENT_SOURCES}} -->
          <p>湖滨休闲道是一条理想的休闲骑行路线，沿途风景秀丽，道路平坦。无论是晨练还是周末出游，这条路线都能带给您轻松愉快的骑行体验。全程沿湖岸线设计，可欣赏湖光山色，适合各年龄段的骑行爱好者。</p>
        </div>
        
        <!-- 折叠面板 - 路线概览 -->
        <div class="collapsible-panel">
          <div class="panel-header">
            <h3><i class="fas fa-info-circle"></i> 路线概览</h3>
            <span>+</span>
            <!-- 折叠面板需添加JS交互 -->
          </div>
          <div class="panel-content">
            <!-- 文字内容来源: {{CONTENT_SOURCES}} -->
            <p>湖滨休闲道全长约12公里，是一条环湖骑行路线。起点位于东湖公园主入口，终点回到起始位置，形成一个完整的环线。</p>
            
            <ul>
              <li><strong>起点:</strong> 东湖公园主入口</li>
              <li><strong>途经:</strong> 湖心岛、观景平台、湿地公园、休闲广场</li>
              <li><strong>终点:</strong> 东湖公园主入口</li>
              <li><strong>推荐骑行方向:</strong> 顺时针</li>
            </ul>
          </div>
        </div>
        
        <!-- 折叠面板 - 海拔剖面 -->
        <div class="collapsible-panel">
          <div class="panel-header">
            <h3><i class="fas fa-chart-area"></i> 海拔剖面</h3>
            <span>+</span>
            <!-- 折叠面板需添加JS交互 -->
          </div>
          <div class="panel-content">
            <div class="elevation-profile">
              <!-- 需接入图表API或使用SVG绘制海拔剖面图 -->
              <!-- 数据来源: {{CONTENT_SOURCES}} -->
              海拔剖面图将在此显示
            </div>
            <!-- 文字内容来源: {{CONTENT_SOURCES}} -->
            <p>这条路线的海拔变化较小，总爬升仅有50米，坡度平缓，很少有明显的上坡路段，非常适合初学者和休闲骑行。</p>
            <ul>
              <li>最低点: 湖边栈道(5m)</li>
              <li>最高点: 观景台(55m)</li>
              <li>平均坡度: 1%</li>
            </ul>
          </div>
        </div>
        
        <!-- 折叠面板 - 路况详情 -->
        <div class="collapsible-panel">
          <div class="panel-header">
            <h3><i class="fas fa-road"></i> 路况详情</h3>
            <span>+</span>
            <!-- 折叠面板需添加JS交互 -->
          </div>
          <div class="panel-content">
            <!-- 文字内容来源: {{CONTENT_SOURCES}} -->
            <p>整体路况良好，以柏油路面为主，少部分路段为平整的砂石路，全程设有专门的自行车道。</p>
            <ul>
              <li><strong>第1-5公里:</strong> 平坦柏油路，自行车专用道宽敞，与步行道分离</li>
              <li><strong>第6-8公里:</strong> 湿地公园区域，砂石路面，路况平整，骑行体验良好</li>
              <li><strong>第9-12公里:</strong> 柏油路面，有部分小型缓坡，视野开阔</li>
            </ul>
            <p><strong>注意事项:</strong> 周末人流量较大，请注意避让行人，尤其是在靠近休闲广场区域。</p>
          </div>
        </div>
        
        <!-- 折叠面板 - 骑行小贴士 -->
        <div class="collapsible-panel">
          <div class="panel-header">
            <h3><i class="fas fa-lightbulb"></i> 骑行小贴士</h3>
            <span>+</span>
            <!-- 折叠面板需添加JS交互 -->
          </div>
          <div class="panel-content">
            <!-- 文字内容来源: {{CONTENT_SOURCES}} -->
            <p>为了让您的骑行更加愉快，我们提供以下建议：</p>
            <ul>
              <li><strong>最佳骑行季节:</strong> 春季(4-5月)和秋季(9-10月)，气温适宜，景色最佳</li>
              <li><strong>最佳骑行时段:</strong> 清晨6-9点或傍晚4-6点，避开烈日和人流高峰</li>
              <li><strong>建议携带:</strong> 水壶、防晒霜、帽子、轻便维修工具、充电宝</li>
              <li><strong>休息点:</strong> 沿途设有多个休息亭和观景台，可适时停留</li>
              <li><strong>拍照推荐:</strong> 湖心岛观景台、日落时的湖面倒影、湿地公园的鸟类</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="info-sidebar">
        <!-- 周边设施板块 -->
        <div class="sidebar-section">
          <h3><i class="fas fa-utensils"></i> 周边设施</h3>
          
          <div class="facilities-cards">
            <!-- 餐饮设施 -->
            <a href="#resource-detail" class="resource-link">
              <div class="facility-card">
                <div class="facility-icon">
                  <i class="fas fa-coffee"></i>
                </div>
                <div class="facility-content">
                  <h4>湖畔咖啡厅</h4>
                  <!-- 文字内容来源: {{CONTENT_SOURCES}} -->
                  <p>位于路线5公里处，提供轻食和饮料</p>
                </div>
              </div>
            </a>
            
            <!-- 维修点 -->
            <div class="facility-card">
              <div class="facility-icon">
                <i class="fas fa-tools"></i>
              </div>
              <div class="facility-content">
                <h4>单车维修站</h4>
                <!-- 文字内容来源: {{CONTENT_SOURCES}} -->
                <p>位于起点和8公里处，提供基础维修工具</p>
              </div>
            </div>
            
            <!-- 厕所 -->
            <div class="facility-card">
              <div class="facility-icon">
                <i class="fas fa-restroom"></i>
              </div>
              <div class="facility-content">
                <h4>公共厕所</h4>
                <!-- 文字内容来源: {{CONTENT_SOURCES}} -->
                <p>沿途设有4处，均有洗手设施</p>
              </div>
            </div>
            
            <!-- 停车场 -->
            <div class="facility-card">
              <div class="facility-icon">
                <i class="fas fa-parking"></i>
              </div>
              <div class="facility-content">
                <h4>停车场</h4>
                <!-- 文字内容来源: {{CONTENT_SOURCES}} -->
                <p>起点附近有大型免费停车场</p>
              </div>
            </div>
            
            <!-- 饮水点 -->
            <div class="facility-card">
              <div class="facility-icon">
                <i class="fas fa-tint"></i>
              </div>
              <div class="facility-content">
                <h4>饮水点</h4>
                <!-- 文字内容来源: {{CONTENT_SOURCES}} -->
                <p>3处直饮水站，可填充水壶</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 天气信息 -->
        <div class="sidebar-section">
          <h3><i class="fas fa-cloud-sun"></i> 今日天气</h3>
          <!-- 需对接天气API -->
          <p>晴朗，22°C-28°C，东北风1-2级</p>
          <p>空气质量: 优 (AQI: 45)</p>
          <p>骑行指数: <strong style="color: #2ecc71;">非常适宜</strong></p>
        </div>
      </div>
    </section>
    
    <section class="gallery-section">
      <h2><i class="fas fa-image"></i> 沿途景点</h2>
      
      <div class="gallery-container">
        <!-- 景点图片1 -->
        <div class="gallery-item">
          <!-- 图片来源: {{CONTENT_SOURCES}} -->
          <!-- 占位符尺寸: 1440×800px -->
          <img src="/source/湖滨休闲道.jpg" alt="湖心岛景色">
          <div class="gallery-caption">湖心岛 - 路线2公里处</div>
        </div>
        
        <!-- 景点图片2 -->
        <div class="gallery-item">
          <!-- 图片来源: {{CONTENT_SOURCES}} -->
          <!-- 占位符尺寸: 1440×800px -->
          <img src="/source/湖滨休闲道.jpg" alt="观景台">
          <div class="gallery-caption">观景台 - 路线4.5公里处</div>
        </div>
        
        <!-- 景点图片3 -->
        <div class="gallery-item">
          <!-- 图片来源: {{CONTENT_SOURCES}} -->
          <!-- 占位符尺寸: 1440×800px -->
          <img src="/source/森林山地线.jpg" alt="湿地公园">
          <div class="gallery-caption">湿地公园 - 路线7公里处</div>
        </div>
        
        <!-- 景点图片4 -->
        <div class="gallery-item">
          <!-- 图片来源: {{CONTENT_SOURCES}} -->
          <!-- 占位符尺寸: 1440×800px -->
          <img src="/source/海岸风景道.jpg" alt="季节性花海">
          <div class="gallery-caption">季节性花海 - 路线9公里处</div>
        </div>
        
        <!-- 景点图片5 -->
        <div class="gallery-item">
          <!-- 图片来源: {{CONTENT_SOURCES}} -->
          <!-- 占位符尺寸: 1440×800px -->
          <img src="/source/湖滨休闲道.jpg" alt="日落湖景">
          <div class="gallery-caption">日落湖景 - 路线11公里处</div>
        </div>
      </div>
    </section>
    
    <!-- 用户交互区域 -->
    <section class="user-actions">
      <div class="action-card">
        <h3><i class="fas fa-star"></i> 路线评价</h3>
        <div class="rating-stars">
          <i class="fas fa-star"></i>
          <i class="fas fa-star"></i>
          <i class="fas fa-star"></i>
          <i class="fas fa-star"></i>
          <i class="far fa-star"></i>
        </div>
        <p>基于126位骑行者的评价</p>
        <button class="btn">写评价</button>
      </div>
      
      <div class="action-card">
        <h3><i class="fas fa-share-alt"></i> 分享路线</h3>
        <p>与好友分享这条美丽路线</p>
        <div class="share-buttons">
          <a href="#" class="share-btn wechat"><i class="fab fa-weixin"></i></a>
          <a href="#" class="share-btn weibo"><i class="fab fa-weibo"></i></a>
          <a href="#" class="share-btn qq"><i class="fab fa-qq"></i></a>
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

.hero h2 {
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
}

.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.6);
  background: linear-gradient(135deg, #FF8A65, #FFB74D);
}

/* 主要内容区域 */
.container {
  padding: 60px 20px;
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

/* 路线卡片容器 */
.route-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 40px;
  margin-top: 60px;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
}

/* 路线卡片样式优化 */
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

/* 难度标签优化 */
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

/* 响应式设计 */
@media (max-width: 768px) {
  .hero {
    padding: 80px 15px 60px;
    min-height: 60vh;
  }
  
  .hero-content {
    padding: 30px 15px;
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