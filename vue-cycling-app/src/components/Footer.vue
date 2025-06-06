<template>
  <footer>
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h4>关于我们</h4>
          <p>自在骑行致力于为骑行爱好者提供高质量的骑行路线推荐和资讯，让每一次骑行都成为难忘的体验。</p>
        </div>
        
        <div class="footer-section">
          <h4>热门路线</h4>
          <div class="footer-routes">
            <div class="footer-route-item">
              <img src="/source/乡村田园路.jpg" alt="乡村田园路">
              <h4>乡村田园路</h4>
              <p class="route-description">穿越古都文化地标，感受历史与现代交融</p>
            </div>
            <div class="footer-route-item">
              <img src="/source/森林山地线.jpg" alt="森林山地线">
              <h4>森林山地线</h4>
              <p class="route-description">挑战专业级越野赛道，体验肾上腺素飙升</p>
            </div>
            <div class="footer-route-item">
              <img src="/source/海岸风景道.jpg" alt="海岸风景道">
              <h4>海岸风景道</h4>
              <p class="route-description">沿着蔚蓝海岸线骑行，沐浴阳光与海风</p>
            </div>
            <div class="footer-route-item">
              <img src="/source/市区文化线.jpg" alt="市区文化线">
              <h4>市区文化线</h4>
              <p class="route-description">漫步城市街道，感受都市生活魅力</p>
            </div>
            <div class="footer-route-item">
              <img src="/source/湖滨休闲道.jpg" alt="湖滨休闲道">
              <h4>湖滨休闲道</h4>
              <p class="route-description">欣赏湖光山色，享受自然美景</p>
            </div>
            
            <div class="more-link-block footer-route-item">
              <router-link to="/vr" class="cta-button">探索更多路线</router-link>
              <div class="more-content">
                <i class="fas fa-arrow-circle-right"></i>
                <h4>探索更多路线</h4>
                <p>发现20+精选骑行路线</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="footer-section">
          <h4>骑行资源</h4>
          <div class="footer-resources">
            <div class="resource-card">
              <div class="resource-image">
                <img src="/source/安全骑行指南.jpg" alt="安全骑行指南">
              </div>
              <div class="resource-content">
                <h3 class="resource-title">安全骑行指南</h3>
                <p class="resource-description">掌握正确骑行姿势与道路安全规范</p>
              </div>
            </div>
            <div class="resource-card">
              <div class="resource-image">
                <img src="/source/骑行装备推荐.jpg" alt="骑行装备">
              </div>
              <div class="resource-content">
                <h3 class="resource-title">骑行装备推荐</h3>
                <p class="resource-description">专业级装备选购指南与使用技巧</p>
              </div>
            </div>
            <div class="resource-card">
              <div class="resource-image">
                <img src="/source/骑行设备保养技巧.jpg" alt="设备保养">
              </div>
              <div class="resource-content">
                <h3 class="resource-title">设备保养技巧</h3>
                <p class="resource-description">延长装备使用寿命的维护秘诀</p>
              </div>
            </div>
            <div class="resource-card">
              <div class="resource-image">
                <img src="/source/骑行活动日历.jpg" alt="活动日历">
              </div>
              <div class="resource-content">
                <h3 class="resource-title">骑行活动日历</h3>
                <p class="resource-description">最新骑行赛事与俱乐部活动安排</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="footer-section">
          <h4>联系我们</h4>
          <ul class="contact-list">
            <li><i class="fas fa-envelope"></i> info@biketrails.com</li>
            <li><i class="fas fa-phone"></i> 400-123-4567</li>
            <li><i class="fas fa-map-marker-alt"></i> 河北经贸大学</li>
          </ul>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; 2025 自在骑行. 保留所有权利.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
// 页脚组件不需要特殊逻辑
</script>

<style scoped>
/* 页脚样式已在全局样式中定义 */
</style>