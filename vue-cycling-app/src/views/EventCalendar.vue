<template>
  <div class="event-calendar">
    <!-- 樱花装饰背景 -->
    <div class="cherry-decoration">
      <div class="floating-petals">
        <img src="/source/floating-sakura.svg" alt="Floating sakura petals" />
      </div>
      <div class="floating-petals-layer2">
        <img src="/source/cherry-petals.svg" alt="Additional petals" />
      </div>
      <img src="/source/cherry-branch.svg" alt="Cherry branch" class="branch-decoration branch-top-left" />
      <img src="/source/cherry-branch.svg" alt="Cherry branch" class="branch-decoration branch-top-right" />
    </div>
    
    <!-- 页面头部 -->
    <section class="hero calendar-hero">
      <div class="hero-content">
        <div class="hero-title-wrapper">
          <img src="/source/cherry-blossom.svg" alt="" class="title-blossom" />
          <h1>骑行活动日历</h1>
          <img src="/source/cherry-blossom.svg" alt="" class="title-blossom" />
        </div>
        <p>最新骑行赛事与俱乐部活动安排，与志同道合的骑友一起享受骑行乐趣</p>
        <div class="hero-stats">
          <div class="stat-item">
            <i class="fas fa-calendar-check"></i>
            <span>精彩活动</span>
          </div>
          <div class="stat-item">
            <i class="fas fa-users"></i>
            <span>骑友聚会</span>
          </div>
          <div class="stat-item">
            <i class="fas fa-trophy"></i>
            <span>专业赛事</span>
          </div>
        </div>
      </div>
    </section>

    <main class="container">
      <!-- 活动筛选 -->
      <section class="filter-section">
        <div class="filter-container">
          <div class="filter-group">
            <label>活动类型：</label>
            <div class="filter-buttons">
              <button 
                v-for="type in eventTypes" 
                :key="type.value"
                :class="['filter-btn', { active: selectedType === type.value }]"
                @click="selectedType = type.value"
              >
                <i :class="type.icon"></i>
                {{ type.label }}
              </button>
            </div>
          </div>
          <div class="filter-group">
            <label>难度等级：</label>
            <div class="filter-buttons">
              <button 
                v-for="level in difficultyLevels" 
                :key="level.value"
                :class="['filter-btn', { active: selectedLevel === level.value }]"
                @click="selectedLevel = level.value"
              >
                <span :class="['difficulty-dot', level.value]"></span>
                {{ level.label }}
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 即将开始的活动 -->
      <section class="upcoming-events">
        <h2 class="section-title">
          <i class="fas fa-clock"></i>
          即将开始的活动
        </h2>
        <div class="events-grid">
          <div 
            v-for="event in filteredUpcomingEvents" 
            :key="event.id"
            class="event-card upcoming"
          >
            <div class="event-date">
              <div class="month">{{ event.month }}</div>
              <div class="day">{{ event.day }}</div>
            </div>
            <div class="event-content">
              <div class="event-header">
                <h3>{{ event.title }}</h3>
                <span :class="['difficulty-badge', event.difficulty]">{{ getDifficultyLabel(event.difficulty) }}</span>
              </div>
              <div class="event-details">
                <div class="detail-item">
                  <i class="fas fa-map-marker-alt"></i>
                  <span>{{ event.location }}</span>
                </div>
                <div class="detail-item">
                  <i class="fas fa-clock"></i>
                  <span>{{ event.time }}</span>
                </div>
                <div class="detail-item">
                  <i class="fas fa-route"></i>
                  <span>{{ event.distance }}</span>
                </div>
                <div class="detail-item">
                  <i class="fas fa-users"></i>
                  <span>{{ event.participants }}/{{ event.maxParticipants }}人</span>
                </div>
              </div>
              <p class="event-description">{{ event.description }}</p>
              <div class="event-actions">
                <button class="btn-primary">立即报名</button>
                <button class="btn-secondary">查看详情</button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 月度日历 -->
      <section class="calendar-section">
        <h2 class="section-title">
          <i class="fas fa-calendar-alt"></i>
          {{ currentMonth }}月活动日历
        </h2>
        <div class="calendar-container">
          <div class="calendar-header">
            <button @click="previousMonth" class="nav-btn">
              <i class="fas fa-chevron-left"></i>
            </button>
            <h3>{{ currentYear }}年{{ currentMonth }}月</h3>
            <button @click="nextMonth" class="nav-btn">
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
          <div class="calendar-grid">
            <div class="weekday" v-for="day in weekdays" :key="day">{{ day }}</div>
            <div 
              v-for="date in calendarDates" 
              :key="date.key"
              :class="['calendar-date', { 
                'other-month': date.otherMonth,
                'today': date.isToday,
                'has-event': date.hasEvent
              }]"
              @click="selectDate(date)"
            >
              <span class="date-number">{{ date.day }}</span>
              <div v-if="date.events" class="event-indicators">
                <span 
                  v-for="event in date.events.slice(0, 3)" 
                  :key="event.id"
                  :class="['event-dot', event.type]"
                  :title="event.title"
                ></span>
                <span v-if="date.events.length > 3" class="more-events">+{{ date.events.length - 3 }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 活动类型介绍 -->
      <section class="event-types">
        <h2 class="section-title">
          <i class="fas fa-list"></i>
          活动类型介绍
        </h2>
        <div class="types-grid">
          <div class="type-card">
            <div class="type-icon">
              <i class="fas fa-trophy"></i>
            </div>
            <h3>竞技赛事</h3>
            <p>专业级别的骑行比赛，包括公路赛、山地赛、计时赛等各种形式的竞技活动。</p>
            <div class="type-features">
              <div class="feature">专业计时</div>
              <div class="feature">奖品丰厚</div>
              <div class="feature">等级认证</div>
            </div>
          </div>
          
          <div class="type-card">
            <div class="type-icon">
              <i class="fas fa-users"></i>
            </div>
            <h3>休闲骑游</h3>
            <p>轻松愉快的集体骑行活动，注重风景欣赏和社交互动，适合各个水平的骑行爱好者。</p>
            <div class="type-features">
              <div class="feature">风景优美</div>
              <div class="feature">节奏轻松</div>
              <div class="feature">社交互动</div>
            </div>
          </div>
          
          <div class="type-card">
            <div class="type-icon">
              <i class="fas fa-graduation-cap"></i>
            </div>
            <h3>技能培训</h3>
            <p>专业教练指导的骑行技能提升课程，包括基础技巧、安全知识、维修保养等内容。</p>
            <div class="type-features">
              <div class="feature">专业指导</div>
              <div class="feature">技能提升</div>
              <div class="feature">安全培训</div>
            </div>
          </div>
          
          <div class="type-card">
            <div class="type-icon">
              <i class="fas fa-heart"></i>
            </div>
            <h3>公益活动</h3>
            <p>结合环保、慈善等公益主题的骑行活动，在享受骑行乐趣的同时为社会贡献力量。</p>
            <div class="type-features">
              <div class="feature">环保主题</div>
              <div class="feature">慈善募捐</div>
              <div class="feature">社会责任</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 热门活动推荐 -->
      <section class="featured-events">
        <h2 class="section-title">
          <i class="fas fa-star"></i>
          热门活动推荐
        </h2>
        <div class="featured-grid">
          <div class="featured-card">
            <div class="featured-image">
              <img src="/source/春季骑行节.jpg" alt="春季骑行节" @error="handleImageError">
              <div class="featured-overlay">
                <span class="featured-tag">热门</span>
              </div>
            </div>
            <div class="featured-content">
              <h3>春季骑行节</h3>
              <p>一年一度的大型骑行盛会，汇聚全国各地的骑行爱好者，多条路线可选。</p>
              <div class="featured-info">
                <div class="info-item">
                  <i class="fas fa-calendar"></i>
                  <span>4月15-16日</span>
                </div>
                <div class="info-item">
                  <i class="fas fa-map-marker-alt"></i>
                  <span>石家庄市区</span>
                </div>
                <div class="info-item">
                  <i class="fas fa-users"></i>
                  <span>预计1000+人参与</span>
                </div>
              </div>
              <button class="btn-featured">了解详情</button>
            </div>
          </div>
          
          <div class="featured-card">
            <div class="featured-image">
              <img src="/source/山地挑战赛.jpg" alt="山地挑战赛" @error="handleImageError">
              <div class="featured-overlay">
                <span class="featured-tag">挑战</span>
              </div>
            </div>
            <div class="featured-content">
              <h3>山地挑战赛</h3>
              <p>专业级山地自行车比赛，考验骑手的技术和体能，设有多个组别。</p>
              <div class="featured-info">
                <div class="info-item">
                  <i class="fas fa-calendar"></i>
                  <span>5月20日</span>
                </div>
                <div class="info-item">
                  <i class="fas fa-map-marker-alt"></i>
                  <span>太行山脉</span>
                </div>
                <div class="info-item">
                  <i class="fas fa-trophy"></i>
                  <span>奖金池10万元</span>
                </div>
              </div>
              <button class="btn-featured">立即报名</button>
            </div>
          </div>
        </div>
      </section>

      <!-- 活动组织指南 -->
      <section class="organize-guide">
        <h2 class="section-title">
          <i class="fas fa-clipboard-list"></i>
          如何组织骑行活动
        </h2>
        <div class="guide-container">
          <div class="guide-step">
            <div class="step-number">1</div>
            <div class="step-content">
              <h3>活动策划</h3>
              <p>确定活动主题、时间、路线和参与人数，制定详细的活动计划和安全预案。</p>
              <ul>
                <li>选择合适的骑行路线</li>
                <li>确定活动时间和集合地点</li>
                <li>制定安全保障措施</li>
                <li>准备必要的装备和物资</li>
              </ul>
            </div>
          </div>
          
          <div class="guide-step">
            <div class="step-number">2</div>
            <div class="step-content">
              <h3>宣传推广</h3>
              <p>通过各种渠道宣传活动，吸引更多骑行爱好者参与，建立活动社群。</p>
              <ul>
                <li>制作精美的活动海报</li>
                <li>在社交媒体平台发布信息</li>
                <li>联系当地骑行俱乐部</li>
                <li>建立活动微信群</li>
              </ul>
            </div>
          </div>
          
          <div class="guide-step">
            <div class="step-number">3</div>
            <div class="step-content">
              <h3>活动执行</h3>
              <p>按照计划组织活动，确保参与者安全，营造良好的活动氛围。</p>
              <ul>
                <li>提前到达集合地点准备</li>
                <li>进行安全说明和路线介绍</li>
                <li>安排领骑和收队人员</li>
                <li>记录活动精彩瞬间</li>
              </ul>
            </div>
          </div>
          
          <div class="guide-step">
            <div class="step-number">4</div>
            <div class="step-content">
              <h3>活动总结</h3>
              <p>活动结束后进行总结，收集参与者反馈，为下次活动积累经验。</p>
              <ul>
                <li>整理活动照片和视频</li>
                <li>收集参与者反馈意见</li>
                <li>总结活动经验教训</li>
                <li>维护参与者关系</li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// 响应式数据
const selectedType = ref('all')
const selectedLevel = ref('all')
const currentYear = ref(2025)
const currentMonth = ref(3)

// 活动类型
const eventTypes = [
  { value: 'all', label: '全部', icon: 'fas fa-list' },
  { value: 'race', label: '竞技赛事', icon: 'fas fa-trophy' },
  { value: 'leisure', label: '休闲骑游', icon: 'fas fa-users' },
  { value: 'training', label: '技能培训', icon: 'fas fa-graduation-cap' },
  { value: 'charity', label: '公益活动', icon: 'fas fa-heart' }
]

// 难度等级
const difficultyLevels = [
  { value: 'all', label: '全部' },
  { value: 'easy', label: '初级' },
  { value: 'medium', label: '中级' },
  { value: 'hard', label: '高级' }
]

// 星期
const weekdays = ['日', '一', '二', '三', '四', '五', '六']

// 即将开始的活动数据
const upcomingEvents = ref([
  {
    id: 1,
    title: '春日踏青骑行',
    type: 'leisure',
    difficulty: 'easy',
    month: '3月',
    day: '25',
    location: '石家庄植物园',
    time: '09:00-12:00',
    distance: '15公里',
    participants: 23,
    maxParticipants: 30,
    description: '春暖花开，与骑友们一起踏青赏花，享受春日美好时光。'
  },
  {
    id: 2,
    title: '山地技能训练',
    type: 'training',
    difficulty: 'medium',
    month: '3月',
    day: '28',
    location: '西山森林公园',
    time: '14:00-17:00',
    distance: '20公里',
    participants: 15,
    maxParticipants: 20,
    description: '专业教练指导山地骑行技巧，提升您的骑行水平。'
  },
  {
    id: 3,
    title: '环保骑行活动',
    type: 'charity',
    difficulty: 'easy',
    month: '4月',
    day: '02',
    location: '滹沱河畔',
    time: '08:00-11:00',
    distance: '12公里',
    participants: 45,
    maxParticipants: 50,
    description: '倡导绿色出行，沿途清理垃圾，保护环境从我做起。'
  },
  {
    id: 4,
    title: '城市挑战赛',
    type: 'race',
    difficulty: 'hard',
    month: '4月',
    day: '08',
    location: '市区环线',
    time: '07:00-10:00',
    distance: '50公里',
    participants: 67,
    maxParticipants: 100,
    description: '城市公路赛，挑战自我，争夺冠军荣誉。'
  }
])

// 计算属性
const filteredUpcomingEvents = computed(() => {
  return upcomingEvents.value.filter(event => {
    const typeMatch = selectedType.value === 'all' || event.type === selectedType.value
    const levelMatch = selectedLevel.value === 'all' || event.difficulty === selectedLevel.value
    return typeMatch && levelMatch
  })
})

const calendarDates = computed(() => {
  const year = currentYear.value
  const month = currentMonth.value
  const firstDay = new Date(year, month - 1, 1)
  const lastDay = new Date(year, month, 0)
  const startDate = new Date(firstDay)
  startDate.setDate(startDate.getDate() - firstDay.getDay())
  
  const dates = []
  const today = new Date()
  
  for (let i = 0; i < 42; i++) {
    const date = new Date(startDate)
    date.setDate(startDate.getDate() + i)
    
    const isCurrentMonth = date.getMonth() === month - 1
    const isToday = date.toDateString() === today.toDateString()
    
    // 模拟一些活动数据
    const events = getEventsForDate(date)
    
    dates.push({
      key: `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`,
      day: date.getDate(),
      otherMonth: !isCurrentMonth,
      isToday,
      hasEvent: events.length > 0,
      events
    })
  }
  
  return dates
})

// 方法
const getDifficultyLabel = (difficulty) => {
  const labels = {
    easy: '初级',
    medium: '中级',
    hard: '高级'
  }
  return labels[difficulty] || difficulty
}

const getEventsForDate = (date) => {
  // 模拟活动数据
  const events = []
  const day = date.getDate()
  
  if (day % 7 === 0) {
    events.push({ id: 1, title: '周末骑游', type: 'leisure' })
  }
  if (day % 10 === 5) {
    events.push({ id: 2, title: '技能培训', type: 'training' })
  }
  if (day === 15) {
    events.push({ id: 3, title: '月度赛事', type: 'race' })
  }
  
  return events
}

const previousMonth = () => {
  if (currentMonth.value === 1) {
    currentMonth.value = 12
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

const nextMonth = () => {
  if (currentMonth.value === 12) {
    currentMonth.value = 1
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

const selectDate = (date) => {
  if (date.hasEvent) {
    console.log('选择日期:', date)
    // 这里可以显示该日期的活动详情
  }
}

const handleImageError = (event) => {
  // 图片加载失败时的处理
  event.target.style.display = 'none'
}

onMounted(() => {
  console.log('骑行活动日历页面已加载')
})
</script>

<style scoped>
.event-calendar {
  min-height: 100vh;
  background: linear-gradient(135deg, #ffdcdc 0%, #ffa7a6 30%, #f9bdc2 60%, #f25477 100%);
  position: relative;
  overflow-x: hidden;
}

/* 樱花装饰背景 */
.cherry-decoration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.floating-petals {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  opacity: 0.8;
  z-index: 1;
}

.floating-petals img {
  position: absolute;
  width: 100%;
  height: auto;
  animation: naturalPetalsFloat 25s infinite linear;
}

@keyframes naturalPetalsFloat {
  0% { 
    transform: translateY(-200px) translateX(0) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  90% {
    opacity: 0.6;
  }
  100% { 
    transform: translateY(calc(100vh + 200px)) translateX(100px) rotate(360deg);
    opacity: 0;
  }
}

/* 添加多个樱花飘落层 */
.floating-petals::before,
.floating-petals::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: url('/source/cherry-petals.svg');
  background-repeat: no-repeat;
  background-size: contain;
  pointer-events: none;
}

.floating-petals::before {
  animation: naturalPetalsFloat 30s infinite linear;
  animation-delay: -10s;
  opacity: 0.5;
  transform: scale(0.8);
}

.floating-petals::after {
  animation: naturalPetalsFloat 35s infinite linear;
  animation-delay: -20s;
  opacity: 0.4;
  transform: scale(0.6) translateX(50px);
}

/* 第二层樱花飘落 */
.floating-petals-layer2 {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  opacity: 0.6;
  z-index: 2;
}

.floating-petals-layer2 img {
  position: absolute;
  width: 100%;
  height: auto;
  animation: gentlePetalsFloat 20s infinite linear;
  animation-delay: -5s;
}

@keyframes gentlePetalsFloat {
  0% { 
    transform: translateY(-150px) translateX(-30px) rotate(0deg) scale(0.8);
    opacity: 0;
  }
  15% {
    opacity: 0.6;
  }
  85% {
    opacity: 0.4;
  }
  100% { 
    transform: translateY(calc(100vh + 150px)) translateX(80px) rotate(270deg) scale(0.8);
    opacity: 0;
  }
}

/* 添加微风摆动效果 */
.cherry-decoration {
  animation: gentleWind 8s infinite ease-in-out;
}

@keyframes gentleWind {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(2px); }
  50% { transform: translateX(-1px); }
  75% { transform: translateX(1px); }
}

.branch-decoration {
  position: absolute;
  width: 300px;
  height: auto;
  opacity: 0.4;
}

.branch-top-left {
  top: 20px;
  left: -50px;
  transform: rotate(-15deg);
}

.branch-top-right {
  top: 20px;
  right: -50px;
  transform: rotate(15deg) scaleX(-1);
}

.calendar-hero {
  background: linear-gradient(135deg, #f25477, #ffa7a6, #ffdcdc);
  color: white;
  padding: 80px 0;
  text-align: center;
  position: relative;
  overflow: hidden;
  z-index: 2;
}

.calendar-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="25" cy="25" r="1" fill="%23ffffff" opacity="0.3"/><circle cx="75" cy="75" r="1.5" fill="%23ffffff" opacity="0.2"/><circle cx="50" cy="10" r="0.8" fill="%23ffffff" opacity="0.4"/></svg>') repeat;
  animation: sparkle 8s infinite ease-in-out;
}

@keyframes sparkle {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.1); }
}

.hero-title-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.title-blossom {
  width: 40px;
  height: 40px;
  animation: blossomRotate 6s infinite ease-in-out;
}

@keyframes blossomRotate {
  0%, 100% { transform: rotate(0deg) scale(1); }
  50% { transform: rotate(10deg) scale(1.1); }
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

.filter-section {
  background: white;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(242, 84, 119, 0.1);
  margin: 40px 0;
  border: 1px solid rgba(255, 182, 193, 0.3);
}

.filter-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.filter-group label {
  font-weight: 600;
  color: #d63384;
  min-width: 80px;
}

.filter-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 20px;
  border: 2px solid #ffb6c1;
  background: white;
  color: #d63384;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.filter-btn:hover {
  background: #ffe4e6;
  transform: translateY(-2px);
}

.filter-btn.active {
  background: linear-gradient(135deg, #f25477, #ffa7a6);
  color: white;
  border-color: #f25477;
}

.difficulty-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.difficulty-dot.easy {
  background: #4CAF50;
}

.difficulty-dot.medium {
  background: #FF9800;
}

.difficulty-dot.hard {
  background: #F44336;
}

.section-title {
  font-size: 2.5rem;
  color: #d63384;
  text-align: center;
  margin-bottom: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.section-title i {
  color: #f25477;
}

.upcoming-events {
  margin: 60px 0;
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 30px;
}

.event-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(242, 84, 119, 0.1);
  transition: all 0.3s ease;
  display: flex;
  border: 2px solid transparent;
}

.event-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(242, 84, 119, 0.2);
  border-color: #f25477;
}

.event-date {
  background: linear-gradient(135deg, #f25477, #ffa7a6);
  color: white;
  padding: 30px 25px;
  text-align: center;
  min-width: 100px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.event-date .month {
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 5px;
}

.event-date .day {
  font-size: 2.5rem;
  font-weight: bold;
}

.event-content {
  padding: 30px;
  flex: 1;
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.event-header h3 {
  color: #d63384;
  font-size: 1.5rem;
  margin: 0;
}

.difficulty-badge {
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.difficulty-badge.easy {
  background: #E8F5E8;
  color: #2E7D32;
}

.difficulty-badge.medium {
  background: #FFF3E0;
  color: #E65100;
}

.difficulty-badge.hard {
  background: #FFEBEE;
  color: #C62828;
}

.event-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #666;
  font-size: 0.9rem;
}

.detail-item i {
  color: #f25477;
  width: 16px;
}

.event-description {
  color: #666;
  line-height: 1.6;
  margin-bottom: 25px;
}

.event-actions {
  display: flex;
  gap: 15px;
}

.btn-primary, .btn-secondary {
  padding: 12px 24px;
  border-radius: 25px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #f25477, #ffa7a6);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(242, 84, 119, 0.4);
}

.btn-secondary {
  background: transparent;
  color: #f25477;
  border: 2px solid #f25477;
}

.btn-secondary:hover {
  background: #f25477;
  color: white;
}

.calendar-section {
  margin: 60px 0;
}

.calendar-container {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(242, 84, 119, 0.1);
  border: 1px solid rgba(255, 182, 193, 0.2);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.calendar-header h3 {
  color: #d63384;
  font-size: 1.5rem;
  margin: 0;
}

.nav-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: linear-gradient(135deg, #f25477, #ffa7a6);
  color: white;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(242, 84, 119, 0.4);
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  background: #ffb6c1;
  border-radius: 10px;
  overflow: hidden;
}

.weekday {
  background: linear-gradient(135deg, #f25477, #ffa7a6);
  color: white;
  padding: 15px;
  text-align: center;
  font-weight: 600;
}

.calendar-date {
  background: white;
  padding: 15px 10px;
  min-height: 80px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.calendar-date:hover {
  background: #ffe4e6;
}

.calendar-date.other-month {
  color: #ccc;
  background: #fafafa;
}

.calendar-date.today {
  background: linear-gradient(135deg, #f25477, #ffa7a6);
  color: white;
}

.calendar-date.has-event {
  background: #ffe4e6;
}

.date-number {
  font-weight: 600;
  display: block;
  margin-bottom: 5px;
}

.event-indicators {
  display: flex;
  flex-wrap: wrap;
  gap: 3px;
}

.event-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.event-dot.race {
  background: #F44336;
}

.event-dot.leisure {
  background: #4CAF50;
}

.event-dot.training {
  background: #FF9800;
}

.event-dot.charity {
  background: #2196F3;
}

.more-events {
  font-size: 0.7rem;
  color: #f25477;
  font-weight: bold;
}

.event-types {
  margin: 60px 0;
}

.types-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
}

.type-card {
  background: white;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(242, 84, 119, 0.1);
  text-align: center;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.type-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(242, 84, 119, 0.2);
  border-color: #f25477;
}

.type-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #f25477, #ffa7a6);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
  font-size: 2rem;
}

.type-card h3 {
  color: #d63384;
  margin-bottom: 15px;
  font-size: 1.3rem;
}

.type-card p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.type-features {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.feature {
  background: #ffe4e6;
  color: #d63384;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
}

.featured-events {
  margin: 60px 0;
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 40px;
}

.featured-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 15px 35px rgba(242, 84, 119, 0.15);
  transition: all 0.3s ease;
}

.featured-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 25px 50px rgba(242, 84, 119, 0.25);
}

.featured-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.featured-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 0.3s ease;
}

.featured-card:hover .featured-image img {
  transform: scale(1.1);
}

.featured-overlay {
  position: absolute;
  top: 15px;
  right: 15px;
}

.featured-tag {
  background: linear-gradient(135deg, #f25477, #ffa7a6);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.featured-content {
  padding: 30px;
}

.featured-content h3 {
  color: #d63384;
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.featured-content p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 25px;
}

.featured-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 25px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #666;
  font-size: 0.9rem;
}

.info-item i {
  color: #f25477;
  width: 16px;
}

.btn-featured {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #f25477, #ffa7a6);
  color: white;
  border: none;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-featured:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(242, 84, 119, 0.4);
}

.organize-guide {
  margin: 60px 0;
}

.guide-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.guide-step {
  background: white;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(242, 84, 119, 0.1);
  display: flex;
  gap: 25px;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 182, 193, 0.2);
}

.guide-step:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(242, 84, 119, 0.2);
}

.step-number {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #f25477, #ffa7a6);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  flex-shrink: 0;
}

.step-content h3 {
  color: #d63384;
  margin-bottom: 15px;
  font-size: 1.3rem;
}

.step-content p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.step-content ul {
  list-style: none;
  padding: 0;
}

.step-content li {
  padding: 5px 0;
  color: #555;
  position: relative;
  padding-left: 20px;
}

.step-content li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #f25477;
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
  
  .filter-container {
    gap: 20px;
  }
  
  .filter-group {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .events-grid {
    grid-template-columns: 1fr;
  }
  
  .event-card {
    flex-direction: column;
  }
  
  .event-date {
    min-width: auto;
    padding: 20px;
  }
  
  .event-details {
    grid-template-columns: 1fr;
  }
  
  .calendar-header {
    flex-direction: column;
    gap: 20px;
  }
  
  .types-grid {
    grid-template-columns: 1fr;
  }
  
  .featured-grid {
    grid-template-columns: 1fr;
  }
  
  .guide-container {
    grid-template-columns: 1fr;
  }
  
  .guide-step {
    flex-direction: column;
    text-align: center;
  }
}
</style>