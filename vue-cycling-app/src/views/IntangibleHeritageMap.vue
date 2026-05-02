<template>
  <div class="heritage-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1><i class="fas fa-map-marked-alt"></i> 非遗骑行地图</h1>
      <p>骑行穿越千年文脉，用车轮丈量非遗之美。精选十条非遗乡村骑行线路，感受传统文化的独特魅力。</p>
    </div>

    <!-- 非遗乡村卡片网格 -->
    <section class="heritage-grid-section">
      <h2 class="section-title"><i class="fas fa-landmark"></i> 十大非遗乡村</h2>
      <div class="heritage-grid">
        <div
          v-for="(item, index) in heritageList"
          :key="index"
          class="heritage-card"
          @click="selectHeritage(item)"
        >
          <div class="heritage-image">
            <img :src="item.image" :alt="item.name" @load="imageLoaded($event)">
            <div class="heritage-tag">{{ item.tag }}</div>
          </div>
          <div class="heritage-content">
            <h3>{{ item.name }}</h3>
            <p class="heritage-desc">{{ item.description }}</p>
            <div class="heritage-meta">
              <span><i class="fas fa-route"></i> {{ item.distance }}</span>
              <span><i class="fas fa-clock"></i> {{ item.time }}</span>
              <span :class="['difficulty', item.difficultyClass]">{{ item.difficulty }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 选中的非遗详情 -->
    <section v-if="selectedHeritage" class="heritage-detail-section">
      <div class="detail-card">
        <div class="detail-header">
          <img :src="selectedHeritage.image" :alt="selectedHeritage.name">
          <div class="detail-header-info">
            <h2>{{ selectedHeritage.name }}</h2>
            <span class="detail-tag">{{ selectedHeritage.tag }}</span>
            <p>{{ selectedHeritage.fullDescription }}</p>
          </div>
        </div>
        <div class="detail-body">
          <div class="detail-stats">
            <div class="stat-item">
              <i class="fas fa-route"></i>
              <h4>骑行距离</h4>
              <p>{{ selectedHeritage.distance }}</p>
            </div>
            <div class="stat-item">
              <i class="far fa-clock"></i>
              <h4>建议用时</h4>
              <p>{{ selectedHeritage.time }}</p>
            </div>
            <div class="stat-item">
              <i class="fas fa-mountain"></i>
              <h4>海拔爬升</h4>
              <p>{{ selectedHeritage.elevation }}</p>
            </div>
            <div class="stat-item">
              <i class="fas fa-star"></i>
              <h4>推荐指数</h4>
              <p>{{ selectedHeritage.rating }}</p>
            </div>
          </div>
          <div class="detail-highlights">
            <h3><i class="fas fa-bullseye"></i> 非遗体验亮点</h3>
            <ul>
              <li v-for="(highlight, idx) in selectedHeritage.highlights" :key="idx">
                {{ highlight }}
              </li>
            </ul>
          </div>
          <div class="detail-tips">
            <h3><i class="fas fa-lightbulb"></i> 骑行贴士</h3>
            <p>{{ selectedHeritage.tips }}</p>
          </div>
        </div>
        <button class="btn btn-close" @click="selectedHeritage = null">
          <i class="fas fa-times"></i> 关闭详情
        </button>
      </div>
    </section>

    <!-- 非遗骑行路线推荐 -->
    <section class="route-recommend-section">
      <h2 class="section-title"><i class="fas fa-bicycle"></i> 非遗骑行路线推荐</h2>
      <div class="route-cards">
        <div class="route-rec-card">
          <div class="route-rec-image">
            <img src="/media/2.jpg" alt="太行水镇线">
          </div>
          <div class="route-rec-content">
            <span class="difficulty easy">初级</span>
            <h3>太行水镇非遗体验线</h3>
            <p>串联太行水镇、恋乡古村与老磨坊，体验河北民俗文化与农耕非遗，全程平缓，适合家庭骑行。</p>
            <div class="route-rec-stats">
              <span><i class="fas fa-route"></i> 18公里</span>
              <span><i class="far fa-clock"></i> 2-3小时</span>
              <span><i class="fas fa-map-marker-alt"></i> 3个非遗点</span>
            </div>
            <button class="btn btn-full" @click="goToRoutePlanning">
              <i class="fas fa-location-arrow"></i> 规划此路线
            </button>
          </div>
        </div>

        <div class="route-rec-card">
          <div class="route-rec-image">
            <img src="/media/17.jpg" alt="碛口古镇线">
          </div>
          <div class="route-rec-content">
            <span class="difficulty moderate">中级</span>
            <h3>碛口古镇晋商文化线</h3>
            <p>穿越碛口古镇、黑龙庙与黄土窑洞群，感受晋商文化与黄河文明，路况起伏，风景壮丽。</p>
            <div class="route-rec-stats">
              <span><i class="fas fa-route"></i> 32公里</span>
              <span><i class="far fa-clock"></i> 4-5小时</span>
              <span><i class="fas fa-map-marker-alt"></i> 4个非遗点</span>
            </div>
            <button class="btn btn-full" @click="goToRoutePlanning">
              <i class="fas fa-location-arrow"></i> 规划此路线
            </button>
          </div>
        </div>

        <div class="route-rec-card">
          <div class="route-rec-image">
            <img src="/media/11.jpg" alt="民俗文化线">
          </div>
          <div class="route-rec-content">
            <span class="difficulty challenging">高级</span>
            <h3>太行民俗深度探索线</h3>
            <p>深度探索二十四节气木版画、吕梁婚俗与太行秧歌，全程串联非遗表演与手工体验点。</p>
            <div class="route-rec-stats">
              <span><i class="fas fa-route"></i> 55公里</span>
              <span><i class="far fa-clock"></i> 6-8小时</span>
              <span><i class="fas fa-map-marker-alt"></i> 5个非遗点</span>
            </div>
            <button class="btn btn-full" @click="goToRoutePlanning">
              <i class="fas fa-location-arrow"></i> 规划此路线
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- 非遗体验互动区 -->
    <section class="interactive-section">
      <div class="action-card">
        <h3><i class="fas fa-calendar-check"></i> 预约非遗体验</h3>
        <p>提前预约乡村非遗手作、民俗表演等深度体验项目</p>
        <button class="btn btn-action" @click="showBooking = true">
          <i class="fas fa-hand-pointer"></i> 立即预约
        </button>
      </div>

      <div class="action-card">
        <h3><i class="fas fa-camera-retro"></i> 骑行打卡挑战</h3>
        <p>集齐10个非遗乡村打卡点，解锁"非遗骑行达人"成就</p>
        <div class="check-progress">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: '0%' }"></div>
          </div>
          <span>0 / 10 已打卡</span>
        </div>
      </div>

      <div class="action-card">
        <h3><i class="fas fa-share-alt"></i> 分享非遗之旅</h3>
        <p>记录并分享您的非遗骑行故事，让更多人感受传统文化之美</p>
        <div class="share-buttons">
          <a href="#" class="share-btn wechat"><i class="fab fa-weixin"></i></a>
          <a href="#" class="share-btn weibo"><i class="fab fa-weibo"></i></a>
          <a href="#" class="share-btn qq"><i class="fab fa-qq"></i></a>
        </div>
      </div>
    </section>

    <!-- 预约弹窗 -->
    <div v-if="showBooking" class="modal-overlay" @click.self="showBooking = false">
      <div class="modal-content">
        <h3><i class="fas fa-calendar-check"></i> 预约非遗体验</h3>
        <div class="form-group">
          <label>选择体验项目</label>
          <select v-model="booking.project">
            <option value="">请选择</option>
            <option value="woodprint">木版画制作体验</option>
            <option value="wedding">吕梁婚俗观礼</option>
            <option value="yangge">太行秧歌学习</option>
            <option value="mill">老磨坊农耕体验</option>
            <option value="opera">黑龙庙戏曲观赏</option>
          </select>
        </div>
        <div class="form-group">
          <label>预约日期</label>
          <input type="date" v-model="booking.date">
        </div>
        <div class="form-group">
          <label>人数</label>
          <input type="number" v-model="booking.people" min="1" max="20">
        </div>
        <div class="form-group">
          <label>联系方式</label>
          <input type="tel" v-model="booking.phone" placeholder="请输入手机号">
        </div>
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="showBooking = false">取消</button>
          <button class="btn btn-primary" @click="submitBooking">确认预约</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedHeritage = ref(null)
const showBooking = ref(false)
const booking = ref({
  project: '',
  date: '',
  people: 1,
  phone: ''
})

const heritageList = ref([
  {
    name: '太行水镇',
    tag: '乡愁民俗',
    image: '/media/2.jpg',
    description: '依托太行山脉，融合传统民俗与现代休闲的文旅小镇。',
    fullDescription: '太行水镇位于河北易县，是一座以太行山水为底色、以乡愁民俗文化为主线的文旅小镇。这里汇聚了太行山区传统建筑风貌，融合了民间手艺、地方美食与民俗表演，是体验河北乡村非遗文化的绝佳之地。',
    distance: '12公里',
    time: '1.5小时',
    difficulty: '初级',
    difficultyClass: 'easy',
    elevation: '80m',
    rating: '★★★★★',
    highlights: ['观看传统民俗表演', '品尝太行特色美食', '体验民间手工艺制作', '漫步易水河畔古街'],
    tips: '建议清晨出发，可先在水镇内享用早餐后再开始骑行。周末人流较多，建议避开高峰期。'
  },
  {
    name: '恋乡古村',
    tag: '传统民居',
    image: '/media/5.jpg',
    description: '保存完好的古村落建筑群，展现太行山区传统民居智慧。',
    fullDescription: '恋乡古村是一处保存完好的太行山区传统村落，石板路、石头房、老槐树构成了一幅古朴的乡村画卷。这里的民居建筑技艺已被列入非遗保护名录，体现了山区人民因地制宜的建筑智慧。',
    distance: '8公里',
    time: '1小时',
    difficulty: '初级',
    difficultyClass: 'easy',
    elevation: '60m',
    rating: '★★★★☆',
    highlights: ['参观古村落建筑群', '了解石头房建造技艺', '体验乡村慢生活', '拍摄古朴田园风光'],
    tips: '村内道路较窄，骑行时请减速慢行，尊重当地居民的生活。'
  },
  {
    name: '老磨坊',
    tag: '农耕文化',
    image: '/media/8.jpg',
    description: '传统水磨与农耕器具展示，体验古老农耕文明。',
    fullDescription: '老磨坊是太行山区传统农耕文化的重要见证，这里保存着古老的水磨、石碾等农耕器具。游客可以亲手操作传统磨坊，感受先人的劳动智慧，了解粮食从田间到餐桌的完整过程。',
    distance: '6公里',
    time: '45分钟',
    difficulty: '初级',
    difficultyClass: 'easy',
    elevation: '40m',
    rating: '★★★★☆',
    highlights: ['亲手操作传统石磨', '了解农耕器具历史', '品尝现磨五谷杂粮', '体验农事劳作乐趣'],
    tips: '磨坊体验活动需提前预约，建议穿着舒适的衣物。'
  },
  {
    name: '二十四节气木版画',
    tag: '民间工艺',
    image: '/media/11.jpg',
    description: '以木板刻画展现中国传统二十四节气文化。',
    fullDescription: '二十四节气木版画是太行山区的传统民间工艺，艺人们在木板上雕刻出每个节气的农事活动与自然景象，再拓印成画。这项技艺将农耕文明与艺术审美完美结合，是非遗保护的重要项目。',
    distance: '10公里',
    time: '1小时',
    difficulty: '初级',
    difficultyClass: 'easy',
    elevation: '50m',
    rating: '★★★★★',
    highlights: ['观看木版画雕刻过程', '亲手制作节气版画', '了解二十四节气文化', '收藏非遗艺术作品'],
    tips: '木版画制作需要耐心，建议预留2-3小时体验时间。'
  },
  {
    name: '易水湖栈道',
    tag: '山水风光',
    image: '/media/14.jpg',
    description: '环湖骑行栈道，欣赏太行山水画卷。',
    fullDescription: '易水湖栈道沿湖而建，是一条专为骑行和步行设计的景观道路。骑行其间，湖光山色尽收眼底，既可以感受大自然的壮美，也能在沿途观景平台了解易水文化的历史典故。',
    distance: '15公里',
    time: '2小时',
    difficulty: '初级',
    difficultyClass: 'easy',
    elevation: '30m',
    rating: '★★★★☆',
    highlights: ['环湖骑行赏景', '打卡湖心观景台', '了解易水文化典故', '拍摄山水风光大片'],
    tips: '栈道部分路段临水，请注意安全。建议携带防晒用品和水壶。'
  },
  {
    name: '碛口古镇客栈',
    tag: '晋商文化',
    image: '/media/17.jpg',
    description: '黄河岸边的明清古镇，晋商文化的活态博物馆。',
    fullDescription: '碛口古镇位于山西临县，曾是黄河水运的重要码头，晋商文化的重要发祥地之一。古镇保存了大量明清时期的商铺、客栈和民居，是研究晋商历史和黄河文明的珍贵遗产。',
    distance: '20公里',
    time: '2.5小时',
    difficulty: '中级',
    difficultyClass: 'moderate',
    elevation: '150m',
    rating: '★★★★★',
    highlights: ['探访明清古客栈', '了解晋商贸易历史', '品尝黄河鲤鱼美食', '夜宿古镇感受历史'],
    tips: '古镇内多为石板路，骑行时请注意路面状况。建议安排一晚住宿，体验古镇夜景。'
  },
  {
    name: '黑龙庙戏台',
    tag: '传统戏曲',
    image: '/media/20.jpg',
    description: '保存完好的明清戏台，传承地方戏曲艺术。',
    fullDescription: '黑龙庙戏台位于碛口古镇制高点，是一座保存完好的明清时期戏台建筑。戏台建筑精美， acoustics 效果极佳，至今仍在演出地方戏曲，是研究中国传统戏曲建筑和表演艺术的重要场所。',
    distance: '22公里',
    time: '3小时',
    difficulty: '中级',
    difficultyClass: 'moderate',
    elevation: '200m',
    rating: '★★★★☆',
    highlights: ['观赏古建筑戏台', '聆听地方戏曲演出', '了解戏曲文化历史', '俯瞰黄河壮丽景色'],
    tips: '戏台演出时间多为节假日，建议提前查询演出安排。登顶需爬坡，体力消耗较大。'
  },
  {
    name: '吕梁婚俗',
    tag: '民俗表演',
    image: '/media/23.jpg',
    description: '独具特色的地方婚礼民俗，热闹喜庆的非遗展演。',
    fullDescription: '吕梁婚俗是山西地区的传统民俗文化，包含迎亲、拜堂、闹洞房等丰富环节。抬花轿、吹唢呐、扭秧歌等表演形式热闹非凡，生动展现了黄土高原人民的热情与豪迈，是非遗表演的重要项目。',
    distance: '18公里',
    time: '2.5小时',
    difficulty: '中级',
    difficultyClass: 'moderate',
    elevation: '120m',
    rating: '★★★★★',
    highlights: ['观看婚俗表演', '参与民俗互动', '了解地方婚嫁文化', '体验传统婚礼服饰'],
    tips: '婚俗表演多集中在特定节日，建议提前咨询活动时间。'
  },
  {
    name: '黄土窑洞群',
    tag: '民居技艺',
    image: '/media/26.jpg',
    description: '依山而建的窑洞村落，展现黄土高原独特居住智慧。',
    fullDescription: '黄土窑洞是黄土高原地区特有的民居形式，具有冬暖夏凉的天然优势。这里的窑洞群依山而建，层次分明，展现了当地人民因地制宜的生存智慧和独特的建筑技艺，是民居类非遗的重要代表。',
    distance: '25公里',
    time: '3.5小时',
    difficulty: '中级',
    difficultyClass: 'moderate',
    elevation: '250m',
    rating: '★★★★☆',
    highlights: ['参观窑洞民居', '了解窑洞建造技艺', '体验窑洞住宿', '感受黄土高原风情'],
    tips: '窑洞住宿体验独特，但设施相对简单，建议提前了解住宿条件。'
  },
  {
    name: '太行秧歌',
    tag: '民间舞蹈',
    image: '/media/29.jpg',
    description: '热情奔放的民间舞蹈，太行山区最具代表性的非遗艺术。',
    fullDescription: '太行秧歌是流行于太行山区的传统民间舞蹈，舞步粗犷有力，节奏明快，充分展现了山区人民乐观豪迈的性格。每逢节庆，村民们身着彩衣、手持彩扇，载歌载舞，是太行山区最具代表性的非遗艺术形式之一。',
    distance: '14公里',
    time: '2小时',
    difficulty: '初级',
    difficultyClass: 'easy',
    elevation: '70m',
    rating: '★★★★★',
    highlights: ['观看原生态秧歌表演', '学习基本秧歌舞步', '了解秧歌文化渊源', '参与节庆狂欢活动'],
    tips: '秧歌表演多在春节和农闲时节，建议关注当地节庆活动安排。'
  }
])

const imageLoaded = (event) => {
  event.target.parentElement.classList.add('loaded')
}

const selectHeritage = (item) => {
  selectedHeritage.value = item
  setTimeout(() => {
    const el = document.querySelector('.heritage-detail-section')
    if (el) {
      window.scrollTo({ top: el.offsetTop - 100, behavior: 'smooth' })
    }
  }, 100)
}

const goToRoutePlanning = () => {
  router.push('/route-planning')
}

const submitBooking = () => {
  if (!booking.value.project || !booking.value.date || !booking.value.phone) {
    alert('请填写完整的预约信息')
    return
  }
  alert('预约成功！我们将尽快与您联系确认。')
  showBooking.value = false
  booking.value = { project: '', date: '', people: 1, phone: '' }
}
</script>

<style scoped>
/* 页面整体布局 */
.heritage-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* 页面标题 */
.page-header {
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.9), rgba(230, 81, 0, 0.7));
  color: white;
  padding: 60px 20px;
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: clamp(2.2rem, 5vw, 3rem);
  margin-bottom: 16px;
  font-weight: 700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.page-header p {
  font-size: clamp(1rem, 2.5vw, 1.2rem);
  opacity: 0.95;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
  max-width: 800px;
  margin: 0 auto;
}

/* 分区标题 */
.section-title {
  text-align: center;
  font-size: clamp(1.8rem, 4vw, 2.4rem);
  margin-bottom: 40px;
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

/* 非遗网格区域 */
.heritage-grid-section {
  padding: 40px 20px;
  max-width: 1400px;
  margin: 0 auto 40px;
}

.heritage-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 50px;
}

/* 非遗卡片 */
.heritage-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  transition: all 0.4s ease;
  cursor: pointer;
  border: 1px solid rgba(255, 152, 0, 0.1);
}

.heritage-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border-color: rgba(255, 152, 0, 0.3);
}

.heritage-image {
  position: relative;
  height: 200px;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  overflow: hidden;
}

.heritage-image::before {
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

.heritage-image.loaded::before {
  display: none;
}

.heritage-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 0.4s ease;
  opacity: 0;
}

.heritage-image.loaded img {
  opacity: 1;
}

.heritage-card:hover .heritage-image img {
  transform: scale(1.05);
}

.heritage-tag {
  position: absolute;
  top: 12px;
  right: 12px;
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  z-index: 2;
}

.heritage-content {
  padding: 24px;
}

.heritage-content h3 {
  font-size: 1.3rem;
  margin-bottom: 10px;
  color: #2C3E50;
  font-weight: 600;
}

.heritage-desc {
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
  font-size: 0.9rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.heritage-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.heritage-meta span {
  font-size: 0.85rem;
  color: #777;
  display: flex;
  align-items: center;
  gap: 4px;
}

.heritage-meta i {
  color: #FF9800;
}

/* 详情区域 */
.heritage-detail-section {
  padding: 0 20px 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.detail-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.detail-header {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 0;
}

.detail-header img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  min-height: 300px;
}

.detail-header-info {
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.detail-header-info h2 {
  font-size: 2rem;
  color: #2C3E50;
  margin-bottom: 12px;
}

.detail-tag {
  display: inline-block;
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 16px;
  width: fit-content;
}

.detail-header-info p {
  color: #666;
  line-height: 1.7;
  font-size: 1rem;
}

.detail-body {
  padding: 40px;
}

.detail-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
  padding: 25px;
  background: #f8f9fa;
  border-radius: 12px;
}

.stat-item {
  text-align: center;
}

.stat-item i {
  font-size: 1.3rem;
  color: #FF9800;
  margin-bottom: 10px;
}

.stat-item h4 {
  font-size: 0.9rem;
  color: #666;
  margin: 8px 0;
  font-weight: 500;
}

.stat-item p {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2C3E50;
  margin: 0;
}

.detail-highlights,
.detail-tips {
  margin-bottom: 25px;
}

.detail-highlights h3,
.detail-tips h3 {
  color: #2C3E50;
  margin-bottom: 15px;
  font-size: 1.2rem;
}

.detail-highlights ul {
  padding-left: 20px;
}

.detail-highlights li {
  margin-bottom: 8px;
  color: #555;
  line-height: 1.6;
}

.detail-tips p {
  color: #666;
  line-height: 1.7;
  padding: 15px;
  background: #FFF8E1;
  border-radius: 8px;
  border-left: 4px solid #FF9800;
}

.btn-close {
  display: block;
  margin: 0 auto 30px;
  padding: 12px 30px;
  background: #e0e0e0;
  color: #555;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-close:hover {
  background: #d0d0d0;
}

/* 路线推荐区域 */
.route-recommend-section {
  padding: 40px 20px;
  max-width: 1400px;
  margin: 0 auto 40px;
}

.route-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  margin-top: 50px;
}

.route-rec-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  transition: all 0.4s ease;
  border: 1px solid rgba(255, 152, 0, 0.1);
}

.route-rec-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 35px rgba(0, 0, 0, 0.15);
}

.route-rec-image {
  height: 220px;
  overflow: hidden;
}

.route-rec-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 0.4s ease;
}

.route-rec-card:hover .route-rec-image img {
  transform: scale(1.05);
}

.route-rec-content {
  padding: 28px;
}

.route-rec-content h3 {
  font-size: 1.4rem;
  color: #2C3E50;
  margin: 12px 0;
  font-weight: 600;
}

.route-rec-content p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.route-rec-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.route-rec-stats span {
  font-size: 0.9rem;
  color: #777;
  display: flex;
  align-items: center;
  gap: 4px;
}

.route-rec-stats i {
  color: #FF9800;
}

/* 交互区域 */
.interactive-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  padding: 0 20px 60px;
  max-width: 1400px;
  margin: 0 auto;
}

.action-card {
  background: white;
  padding: 35px;
  border-radius: 16px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: all 0.3s ease;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
}

.action-card h3 {
  color: #2C3E50;
  margin-bottom: 12px;
  font-size: 1.2rem;
}

.action-card h3 i {
  color: #FF9800;
  margin-right: 8px;
}

.action-card p {
  color: #666;
  margin-bottom: 20px;
  line-height: 1.6;
}

.btn-action {
  padding: 12px 28px;
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-action:hover {
  background: linear-gradient(135deg, #FFB74D, #FF9800);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 152, 0, 0.4);
}

.check-progress {
  margin-top: 15px;
}

.progress-bar {
  width: 100%;
  height: 10px;
  background: #e0e0e0;
  border-radius: 5px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #FF9800, #F57C00);
  border-radius: 5px;
  transition: width 0.5s ease;
}

.check-progress span {
  font-size: 0.9rem;
  color: #666;
}

.share-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.share-btn {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.share-btn:hover {
  transform: translateY(-3px);
}

.share-btn.wechat {
  background: #07C160;
}

.share-btn.weibo {
  background: #E6162D;
}

.share-btn.qq {
  background: #12B7F5;
}

/* 按钮通用样式 */
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

/* 难度标签 */
.difficulty {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.difficulty.easy {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
}

.difficulty.moderate {
  background: linear-gradient(135deg, #FF9800, #FFB74D);
  color: white;
}

.difficulty.challenging {
  background: linear-gradient(135deg, #F44336, #E57373);
  color: white;
}

/* 弹窗 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  padding: 35px;
  border-radius: 16px;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
}

.modal-content h3 {
  color: #2C3E50;
  margin-bottom: 25px;
  text-align: center;
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  color: #555;
  font-weight: 500;
  font-size: 0.9rem;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #FF9800;
  box-shadow: 0 0 0 3px rgba(255, 152, 0, 0.1);
}

.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 25px;
}

.modal-actions .btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary {
  background: #e0e0e0;
  color: #555;
}

.btn-secondary:hover {
  background: #d0d0d0;
}

.btn-primary {
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #FFB74D, #FF9800);
}

/* 动画 */
@keyframes spin {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

/* 响应式 */
@media (max-width: 768px) {
  .heritage-grid {
    grid-template-columns: 1fr;
  }

  .detail-header {
    grid-template-columns: 1fr;
  }

  .detail-header img {
    height: 220px;
  }

  .detail-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .route-cards {
    grid-template-columns: 1fr;
  }

  .interactive-section {
    grid-template-columns: 1fr;
  }
}
</style>
