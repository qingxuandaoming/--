<template>
  <main class="container">
    <div class="vr-container">
      <div class="vr-header">
        <h1>VR灵境体验</h1>
        <p>通过虚拟现实技术，提前体验精选骑行路线的美景与挑战，让您足不出户就能感受骑行乐趣</p>
        <a href="#vr-routes" class="cta-button">探索VR路线</a>
      </div>
      
      <div id="vr-routes" class="vr-routes">
        <div class="vr-route-card" v-for="(route, index) in vrRoutes" :key="index">
          <div class="vr-route-image">
            <img :src="route.image" :alt="route.title">
            <span class="vr-badge">{{ route.badge }}</span>
          </div>
          <div class="vr-route-content">
            <h3 class="vr-route-title">{{ route.title }}</h3>
            <p class="vr-route-description">{{ route.description }}</p>
            
            <div class="vr-route-stats">
              <div class="vr-stat">
                <i class="fas fa-route"></i>
                <span>{{ route.distance }}</span>
              </div>
              <div class="vr-stat">
                <i class="fas fa-mountain"></i>
                <span>{{ route.elevation }}</span>
              </div>
              <div class="vr-stat">
                <i class="fas fa-eye"></i>
                <span>{{ route.views }}</span>
              </div>
            </div>
            
            <a :href="route.link" class="vr-btn">开始VR体验</a>
          </div>
        </div>
      </div>
      
      <div class="vr-experience">
        <h2>VR体验如何工作？</h2>
        
        <div class="vr-experience-content">
          <div class="vr-experience-image">
            <img src="/source/1.jpg" alt="VR体验示意图">
          </div>
          
          <div class="vr-experience-text">
            <div class="vr-step">
              <div class="vr-step-number">1</div>
              <div class="vr-step-content">
                <h3>选择路线</h3>
                <p>从我们精心挑选的VR路线中选择您感兴趣的线路</p>
              </div>
            </div>
            
            <div class="vr-step">
              <div class="vr-step-number">2</div>
              <div class="vr-step-content">
                <h3>准备设备</h3>
                <p>使用VR头盔获得最佳体验，或直接使用手机/电脑浏览</p>
              </div>
            </div>
            
            <div class="vr-step">
              <div class="vr-step-number">3</div>
              <div class="vr-step-content">
                <h3>沉浸体验</h3>
                <p>360°全景视图，让您身临其境感受骑行路线的美景</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="vr-devices">
        <h2>支持的设备</h2>
        
        <div class="vr-device-list">
          <div class="vr-device">
            <div class="vr-device-icon">
              <i class="fas fa-vr-cardboard"></i>
            </div>
            <h3>VR头盔</h3>
            <p>Oculus Quest, HTC Vive, PlayStation VR等</p>
          </div>
          
          <div class="vr-device">
            <div class="vr-device-icon">
              <i class="fas fa-mobile-alt"></i>
            </div>
            <h3>智能手机</h3>
            <p>支持陀螺仪功能的iOS/Android设备</p>
          </div>
          
          <div class="vr-device">
            <div class="vr-device-icon">
              <i class="fas fa-laptop"></i>
            </div>
            <h3>电脑</h3>
            <p>现代浏览器支持的Windows/Mac设备</p>
          </div>
        </div>
      </div>
      
      <div class="vr-faq">
        <h2>常见问题</h2>
        
        <div class="vr-faq-item" v-for="(faq, index) in faqs" :key="index">
          <div class="vr-faq-question" @click="toggleFaq(index)" :class="{ active: activeFaq === index }">
            {{ faq.question }}
            <i class="fas fa-chevron-down"></i>
          </div>
          <div class="vr-faq-answer" :class="{ active: activeFaq === index }">
            {{ faq.answer }}
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue';

const activeFaq = ref(null);

const vrRoutes = [
  {
    title: '湖滨休闲VR体验',
    description: '沿湖岸骑行的平缓路线，欣赏湖光山色，感受微风拂面的惬意',
    image: '/public/source/湖滨休闲道.jpg',
    badge: '热门',
    distance: '12公里',
    elevation: '50m',
    views: '2.5k次观看',
    link: '#'
  },
  {
    title: '森林山地VR挑战',
    description: '穿越茂密森林的山地路线，体验起伏多变的地形和清新的森林空气',
    image: '/public/source/森林山地线.jpg',
    badge: '新上线',
    distance: '25公里',
    elevation: '320m',
    views: '1.8k次观看',
    link: '#'
  },
  {
    title: '海岸风景VR之旅',
    description: '沿海岸线蜿蜒的挑战性路线，欣赏壮观的海洋景色，感受海风的力量',
    image: '/public/source/海岸风景道.jpg',
    badge: '挑战',
    distance: '40公里',
    elevation: '580m',
    views: '3.2k次观看',
    link: '#'
  }
];

const faqs = [
  {
    question: '我需要什么设备才能体验VR骑行？',
    answer: '您可以使用VR头盔(如Oculus Quest)获得最佳体验，也可以使用支持陀螺仪的智能手机，或者直接在电脑浏览器中以普通模式观看。'
  },
  {
    question: 'VR体验是否需要付费？',
    answer: '基础VR路线体验是免费的，高级路线和特殊体验可能需要会员资格或单独付费。详情请查看各路线的说明。'
  },
  {
    question: '如何获得最佳VR体验效果？',
    answer: '建议使用VR头盔，在安静、空间充足的环境中体验。使用手机时，请站立并缓慢转动身体以获得360°视图。确保网络连接良好以获得高质量视频流。'
  },
  {
    question: '我可以下载VR内容离线观看吗？',
    answer: '目前VR内容仅支持在线观看。我们计划在未来版本中添加下载功能，敬请期待。'
  }
];

const toggleFaq = (index) => {
  if (activeFaq.value === index) {
    activeFaq.value = null;
  } else {
    activeFaq.value = index;
  }
};
</script>

<style scoped>
.vr-container {
  max-width: 1000px;
  margin: 60px auto;
}

.vr-header {
  text-align: center;
  margin-bottom: 50px;
}

.vr-header h1 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 2.5rem;
}

.vr-header p {
  color: #7f8c8d;
  font-size: 1.1rem;
  max-width: 700px;
  margin: 0 auto 30px;
  line-height: 1.6;
}

.vr-routes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 50px;
}

.vr-route-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.vr-route-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.vr-route-image {
  height: 200px;
  overflow: hidden;
  position: relative;
}

.vr-route-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.vr-route-card:hover .vr-route-image img {
  transform: scale(1.1);
}

.vr-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(255, 152, 0, 0.9);
  color: white;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.vr-route-content {
  padding: 25px;
}

.vr-route-title {
  font-size: 1.3rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.vr-route-description {
  color: #7f8c8d;
  margin-bottom: 20px;
  line-height: 1.5;
}

.vr-route-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  font-size: 0.9rem;
}

.vr-stat {
  display: flex;
  align-items: center;
  color: #7f8c8d;
}

.vr-stat i {
  color: #F57C00;
  margin-right: 5px;
}

.vr-btn {
  display: inline-block;
  padding: 10px 20px;
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  border-radius: 30px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  text-align: center;
  width: 100%;
}

.vr-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(255, 152, 0, 0.4);
}

.vr-experience {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 50px;
}

.vr-experience h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  text-align: center;
}

.vr-experience-content {
  display: flex;
  align-items: center;
  gap: 40px;
}

.vr-experience-image {
  flex: 1;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.vr-experience-image img {
  width: 100%;
  height: auto;
  display: block;
}

.vr-experience-text {
  flex: 1;
}

.vr-step {
  display: flex;
  margin-bottom: 25px;
}

.vr-step-number {
  width: 40px;
  height: 40px;
  background: #FF9800;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  margin-right: 15px;
  flex-shrink: 0;
}

.vr-step-content h3 {
  color: #2c3e50;
  margin-bottom: 5px;
}

.vr-step-content p {
  color: #7f8c8d;
  line-height: 1.5;
}

.vr-devices {
  margin-bottom: 50px;
}

.vr-devices h2 {
  color: #2c3e50;
  margin-bottom: 30px;
  text-align: center;
}

.vr-device-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.vr-device {
  background: white;
  border-radius: 12px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.vr-device:hover {
  transform: translateY(-5px);
}

.vr-device-icon {
  width: 70px;
  height: 70px;
  background: rgba(255, 152, 0, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.vr-device-icon i {
  font-size: 30px;
  color: #FF9800;
}

.vr-device h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.vr-device p {
  color: #7f8c8d;
}

.vr-faq {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}

.vr-faq h2 {
  color: #2c3e50;
  margin-bottom: 30px;
  text-align: center;
}

.vr-faq-item {
  margin-bottom: 15px;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}

.vr-faq-question {
  padding: 18px 20px;
  background: #f8f9fa;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.3s ease;
  font-weight: 500;
  color: #2c3e50;
}

.vr-faq-question:hover {
  background: #e9ecef;
}

.vr-faq-question i {
  transition: transform 0.3s ease;
}

.vr-faq-question.active i {
  transform: rotate(180deg);
}

.vr-faq-answer {
  padding: 0 20px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease, padding 0.3s ease;
  color: #7f8c8d;
  line-height: 1.6;
}

.vr-faq-question.active + .vr-faq-answer {
  max-height: 500px;
  padding: 20px;
}

@media (max-width: 768px) {
  .vr-experience-content {
    flex-direction: column;
  }
  
  .vr-experience-image,
  .vr-experience-text {
    width: 100%;
  }
}
</style>