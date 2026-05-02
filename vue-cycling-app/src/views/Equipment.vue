<template>
  <div class="equipment-page">
    <!-- 页面头部 -->
    <section class="hero">
      <div class="hero-content">
        <h1>骑行装备推荐</h1>
        <p>精选优质骑行装备，为您的骑行之旅保驾护航</p>
      </div>
    </section>

    <main class="container">
      <!-- 启星装备推荐 -->
      <section class="featured-section">
        <div class="featured-section-header">
          <div class="featured-badge">
            <i class="fas fa-crown"></i>
            <span>启星精选</span>
          </div>
          <h2>启星装备推荐</h2>
          <p class="featured-subtitle">前沿科技装备，重新定义骑行体验</p>
        </div>
        
        <div class="featured-grid">
          <!-- 头盔产品 -->
          <div class="featured-card">
            <div class="featured-card-header">
              <div class="featured-icon helmet-icon">
                <i class="fas fa-hard-hat"></i>
              </div>
              <div class="featured-title-area">
                <h3>混天AI骑行头盔</h3>
                <div class="featured-tags">
                  <span class="featured-tag tag-radar">77GHz雷达</span>
                  <span class="featured-tag tag-ai">端侧AI</span>
                  <span class="featured-tag tag-ar">AR显示</span>
                  <span class="featured-tag tag-npu">10T NPU</span>
                </div>
              </div>
            </div>
            
            <div class="featured-images">
              <div class="featured-img-wrapper">
                <img src="/source/头盔爆炸图.png" alt="混天AI骑行头盔-爆炸图">
                <div class="img-caption">结构爆炸图</div>
              </div>
              <div class="featured-img-wrapper">
                <img src="/source/带字头盔爆炸图.png" alt="混天AI骑行头盔-详解图">
                <div class="img-caption">技术详解图</div>
              </div>
            </div>
            
            <div class="featured-content">
              <div class="feature-block">
                <h4><i class="fas fa-radar"></i> 全域感知预警</h4>
                <p>内嵌 <strong>77GHz 毫米波雷达</strong>，150 米后方追踪，端侧 AI 预判超车意图，精准区分同向超车与交叉风险。6 麦克风阵列 + 骨传导，不做普通听歌，而是<strong>重建空间声场</strong>——夯土号子如哪吒混天绫般缠绕方位，戏曲混响随位置漂移，HRTF 头部传输函数让声音具备空间锚定。</p>
              </div>
              <div class="feature-block">
                <h4><i class="fas fa-microchip"></i> 端侧算力引擎</h4>
                <p>高通 QCC / BES 系列 NPU，<strong>10T 算力全部本地运行</strong>，山区无信号照常预警，隐私数据不出盔。</p>
              </div>
              <div class="feature-block">
                <h4><i class="fas fa-eye"></i> 天眼视界考古透镜</h4>
                <p>双目衍射光波导 + 全彩 MicroLED，<strong>3000 尼特户外可用</strong>。镜片左半边是残垣断壁，右半边 AI 实时叠加完整古建——如同姜子牙元神法相，让消逝的历史在眼前重构。SLAM + 3DGS 端侧跑通，虚实光照一致。显示区域锁死镜片下方 20%，路口自动降亮度。<strong>瞳孔追踪</strong>实现看一眼即操作，双手不离把。</p>
              </div>
            </div>
          </div>
          
          <!-- 眼镜产品 -->
          <div class="featured-card">
            <div class="featured-card-header">
              <div class="featured-icon glasses-icon">
                <i class="fas fa-glasses"></i>
              </div>
              <div class="featured-title-area">
                <h3>启星智能骑行眼镜</h3>
                <div class="featured-tags">
                  <span class="featured-tag tag-hud">HUD显示</span>
                  <span class="featured-tag tag-lens">光致变色</span>
                  <span class="featured-tag tag-nav">智能导航</span>
                  <span class="featured-tag tag-audio">定向音频</span>
                </div>
              </div>
            </div>
            
            <div class="featured-images">
              <div class="featured-img-wrapper">
                <img src="/source/眼镜.webp" alt="启星智能骑行眼镜-外观">
                <div class="img-caption">全景外观</div>
              </div>
              <div class="featured-img-wrapper">
                <img src="/source/眼镜2.webp" alt="启星智能骑行眼镜-细节">
                <div class="img-caption">细节特写</div>
              </div>
            </div>
            
            <div class="featured-content">
              <div class="feature-block">
                <h4><i class="fas fa-tachometer-alt"></i> HUD抬头显示</h4>
                <p>轻量化钛合金镜架，搭配<strong>光致变色镜片</strong>，全天候自适应光线变化。内置微型 HUD 投影系统，实时显示速度、踏频、心率与导航路径，<strong>视线无需离开路面</strong>，安全与信息兼得。</p>
              </div>
              <div class="feature-block">
                <h4><i class="fas fa-bluetooth-b"></i> 智能互联生态</h4>
                <p>蓝牙 5.3 双模连接，支持多设备协同。开放式<strong>定向音频</strong>设计，环境感知与音乐享受兼得，骑行中既能聆听节拍，又不隔绝外界警示。</p>
              </div>
              <div class="feature-block">
                <h4><i class="fas fa-battery-full"></i> 全天候耐久</h4>
                <p><strong>IPX7 级防水</strong>，暴雨骑行无惧挑战。超长续航 18 小时，长途骑行一镜到底。磁吸快充电极，1 小时回血 80%，告别电量焦虑。</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 搜索和筛选区域 -->
      <section class="search-section">
        <div class="search-bar">
          <div class="search-input-wrapper" :class="{ 'dropdown-open': showSearchSuggestions }">
            <i class="fas fa-search"></i>
            <input 
              type="text" 
              v-model="searchKeyword" 
              placeholder="搜索装备名称、品牌或型号..."
              class="search-input"
              @keyup.enter="searchEquipment"
              @focus="showSearchSuggestions = true; filterSuggestions()"
              @blur="hideSearchSuggestions"
              @input="filterSuggestions"
            >
            <button @click="searchEquipment" class="search-btn">搜索</button>
            
            <!-- 搜索建议下拉菜单 -->
            <div v-if="showSearchSuggestions" class="search-suggestions">
              <div class="suggestions-header">热门搜索建议</div>
              <div 
                v-for="suggestion in filteredSuggestions" 
                :key="suggestion"
                class="suggestion-item"
                @mousedown="selectSuggestion(suggestion)"
              >
                <i class="fas fa-search suggestion-icon"></i>
                <span>{{ suggestion }}</span>
              </div>
              <div v-if="filteredSuggestions.length === 0" class="no-suggestions">
                暂无相关建议
              </div>
            </div>
          </div>
        </div>
        
        <div class="filters">
          <div class="filter-group">
            <label>分类:</label>
            <select v-model="selectedCategory" @change="searchEquipment">
              <option value="">全部分类</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>
          
          <div class="filter-group">
            <label>价格范围:</label>
            <select v-model="priceRange" @change="searchEquipment">
              <option value="">不限</option>
              <option value="0-100">100元以下</option>
              <option value="100-500">100-500元</option>
              <option value="500-1000">500-1000元</option>
              <option value="1000-2000">1000-2000元</option>
              <option value="2000-5000">2000-5000元</option>
              <option value="5000-">5000元以上</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label>平台:</label>
            <select v-model="selectedPlatform" @change="searchEquipment">
              <option value="">全部平台</option>
              <option value="天猫">天猫</option>
              <option value="京东">京东</option>
              <option value="淘宝">淘宝</option>
            </select>
          </div>
        </div>
      </section>

      <!-- 装备列表 -->
      <section class="equipment-section">
        <div class="section-header">
          <h2>推荐装备</h2>
          <div class="sort-options">
            <label>排序:</label>
            <select v-model="sortBy" @change="searchEquipment">
              <option value="rating">评分优先</option>
              <option value="price_asc">价格从低到高</option>
              <option value="price_desc">价格从高到低</option>
              <option value="newest">最新发布</option>
            </select>
          </div>
        </div>
        
        <!-- 加载状态 -->
        <div v-if="loading" class="loading">
          <i class="fas fa-spinner fa-spin"></i>
          <p>正在加载装备信息...</p>
        </div>
        
        <!-- 装备网格 -->
        <div v-else-if="equipmentList.length > 0" class="equipment-grid">
          <div 
            v-for="equipment in equipmentList" 
            :key="equipment.id" 
            class="equipment-card"
            @click="viewEquipmentDetail(equipment)"
          >
            <div class="equipment-image">
              <img 
                :src="equipment.images && equipment.images.length > 0 ? equipment.images[0] : '/source/default-equipment.jpg'" 
                :alt="equipment.name"
                @error="handleImageError"
              >
              <div class="equipment-badge" v-if="equipment.rating >= 4.5">
                <i class="fas fa-star"></i>
                推荐
              </div>
            </div>
            
            <div class="equipment-content">
              <div class="equipment-header">
                <h3>{{ equipment.name }}</h3>
                <div class="brand" v-if="equipment.brand">{{ equipment.brand }}</div>
              </div>
              
              <div class="equipment-rating" v-if="equipment.rating > 0">
                <div class="stars">
                  <i 
                    v-for="i in 5" 
                    :key="i" 
                    :class="['fas fa-star', { 'active': i <= Math.round(equipment.rating) }]"
                  ></i>
                </div>
                <span class="rating-text">{{ (Number(equipment.rating) || 0).toFixed(1) }} ({{ Number(equipment.review_count) || 0 }}评价)</span>
              </div>
              
              <div class="equipment-description">
                <p>{{ equipment.description || '暂无描述' }}</p>
              </div>
              
              <div class="equipment-price" v-if="equipment.latest_price">
                <div class="current-price">¥{{ equipment.latest_price.price }}</div>
                <div class="platform">{{ equipment.latest_price.platform }}</div>
              </div>
              
              <div class="equipment-tags" v-if="equipment.tags && equipment.tags.length > 0">
                <span 
                  v-for="tag in equipment.tags.slice(0, 3)" 
                  :key="tag" 
                  class="tag"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div v-else class="empty-state">
          <i class="fas fa-search"></i>
          <h3>未找到相关装备</h3>
          <p>请尝试调整搜索条件或筛选器</p>
        </div>
        
        <!-- 分页 -->
        <div v-if="totalPages > 1" class="pagination">
          <button 
            @click="changePage(currentPage - 1)" 
            :disabled="currentPage <= 1"
            class="page-btn"
          >
            <i class="fas fa-chevron-left"></i>
          </button>
          
          <span class="page-info">
            第 {{ currentPage }} 页，共 {{ totalPages }} 页
          </span>
          
          <button 
            @click="changePage(currentPage + 1)" 
            :disabled="currentPage >= totalPages"
            class="page-btn"
          >
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </section>
      
      <!-- 数据分析区域 -->
      <section class="analytics-section">
        <div class="section-header">
          <h2>数据分析</h2>
          <p>深入了解骑行装备市场趋势和价格分析</p>
        </div>
        
        <div class="analytics-grid">
          <!-- 价格历史趋势 -->
          <div class="analytics-card full-width">
            <PriceHistoryChart 
              title="热门产品价格历史趋势" 
              :equipment-id="'sample-helmet-001'"
            />
          </div>
          
          <!-- 品牌市场份额和价格分布 -->
          <div class="analytics-row">
            <div class="analytics-card">
              <BrandMarketShareChart 
                title="品牌市场份额分析" 
                :category-id="selectedCategory || 'all'"
              />
            </div>
            <div class="analytics-card">
              <PriceDistributionChart 
                title="价格分布统计" 
                :category-id="selectedCategory || 'all'"
              />
            </div>
          </div>
          
          <!-- 品牌综合评分对比 -->
          <div class="analytics-card full-width">
            <BrandRadarChart 
              title="品牌综合评分对比" 
              :category="selectedCategory || 'helmet'"
            />
          </div>
        </div>
      </section>
    </main>
    
    <!-- 装备详情模态框 -->
    <div v-if="showDetailModal" class="modal-overlay" @click="closeDetailModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ selectedEquipment.name }}</h2>
          <button @click="closeDetailModal" class="close-btn">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="equipment-detail">
            <div class="detail-images">
              <img 
                :src="selectedEquipment.images && selectedEquipment.images.length > 0 ? selectedEquipment.images[0] : '/source/default-equipment.jpg'" 
                :alt="selectedEquipment.name"
                @error="handleImageError"
              >
            </div>
            
            <div class="detail-info">
              <div class="basic-info">
                <h3>基本信息</h3>
                <div class="info-item" v-if="selectedEquipment.brand">
                  <label>品牌:</label>
                  <span>{{ selectedEquipment.brand }}</span>
                </div>
                <div class="info-item" v-if="selectedEquipment.model">
                  <label>型号:</label>
                  <span>{{ selectedEquipment.model }}</span>
                </div>
                <div class="info-item" v-if="selectedEquipment.category_name">
                  <label>分类:</label>
                  <span>{{ selectedEquipment.category_name }}</span>
                </div>
                <div class="info-item" v-if="selectedEquipment.weight">
                  <label>重量:</label>
                  <span>{{ selectedEquipment.weight }}g</span>
                </div>
                <div class="info-item" v-if="selectedEquipment.material">
                  <label>材质:</label>
                  <span>{{ selectedEquipment.material }}</span>
                </div>
              </div>
              
              <div class="specifications" v-if="selectedEquipment.specifications">
                <h3>规格参数</h3>
                <div class="spec-grid">
                  <div 
                    v-for="(value, key) in selectedEquipment.specifications" 
                    :key="key" 
                    class="spec-item"
                  >
                    <label>{{ key }}:</label>
                    <span>{{ value }}</span>
                  </div>
                </div>
              </div>
              
              <div class="description" v-if="selectedEquipment.description">
                <h3>产品描述</h3>
                <p>{{ selectedEquipment.description }}</p>
              </div>
              
              <div class="price-info" v-if="selectedEquipment.latest_price">
                <h3>价格信息</h3>
                <div class="price-display">
                  <span class="price">¥{{ selectedEquipment.latest_price.price }}</span>
                  <span class="platform">{{ selectedEquipment.latest_price.platform }}</span>
                </div>
                <a 
                  v-if="selectedEquipment.latest_price.url" 
                  :href="selectedEquipment.latest_price.url" 
                  target="_blank" 
                  class="buy-btn"
                >
                  <i class="fas fa-external-link-alt"></i>
                  前往购买
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import ApiService from '@/services/api.js'
import PriceHistoryChart from '@/components/PriceHistoryChart.vue'
import BrandMarketShareChart from '@/components/BrandMarketShareChart.vue'
import PriceDistributionChart from '@/components/PriceDistributionChart.vue'
import BrandRadarChart from '@/components/BrandRadarChart.vue'

export default {
  name: 'Equipment',
  components: {
    PriceHistoryChart,
    BrandMarketShareChart,
    PriceDistributionChart,
    BrandRadarChart
  },
  setup() {
    // 响应式数据
    const loading = ref(false)
    const searchKeyword = ref('')
    const selectedCategory = ref('')
    const priceRange = ref('')
    const selectedPlatform = ref('')
    const sortBy = ref('rating')
    const currentPage = ref(1)
    const perPage = ref(12)
    
    const categories = ref([])
    const equipmentList = ref([])
    const totalItems = ref(0)
    const totalPages = ref(0)
    
    const showDetailModal = ref(false)
    const selectedEquipment = ref({})
    
    // 搜索建议相关
    const showSearchSuggestions = ref(false)
    const searchSuggestions = ref([
      '山地车',
      '公路车',
      '折叠车',
      '电动车',
      '骑行头盔',
      '骑行服',
      '骑行手套',
      '骑行眼镜',
      '车灯',
      '水壶',
      '码表',
      '车锁',
      '捷安特',
      '美利达',
      '喜德盛',
      'Trek',
      'Giant',
      'Specialized'
    ])
    const filteredSuggestions = ref([])
    
    // 计算属性
    const priceFilter = computed(() => {
      if (!priceRange.value) return { min: null, max: null }
      
      const [min, max] = priceRange.value.split('-')
      return {
        min: min && !isNaN(parseFloat(min)) ? parseFloat(min) : null,
        max: max && !isNaN(parseFloat(max)) ? parseFloat(max) : null
      }
    })
    
    // 方法
    const loadCategories = async () => {
      try {
        const response = await ApiService.equipment.getCategories()
        if (response && response.success) {
          categories.value = response.data || []
        }
      } catch (error) {
        console.error('加载分类失败:', error)
        categories.value = []
      }
    }
    
    const searchEquipment = async () => {
      loading.value = true
      try {
        const params = {
          keyword: searchKeyword.value,
          category_id: selectedCategory.value || null,
          min_price: priceFilter.value.min,
          max_price: priceFilter.value.max,
          platform: selectedPlatform.value || null,
          page: currentPage.value,
          per_page: perPage.value,
          sort_by: sortBy.value
        }
        
        console.log('搜索参数:', params)
        const response = await ApiService.equipment.search(params)
        console.log('API响应完整内容:', JSON.stringify(response, null, 2))
        
        if (response && response.success && response.data) {
          equipmentList.value = response.data.items || []
          totalItems.value = response.data.total || 0
          totalPages.value = response.data.pages || 0
          console.log('搜索成功，找到', equipmentList.value.length, '条记录')
        } else {
          console.error('API响应失败，完整响应:', JSON.stringify(response, null, 2))
          equipmentList.value = []
          totalItems.value = 0
          totalPages.value = 0
        }
      } catch (error) {
        console.error('搜索装备失败:', error)
        equipmentList.value = []
        totalItems.value = 0
        totalPages.value = 0
      } finally {
        loading.value = false
      }
    }
    
    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        searchEquipment()
      }
    }
    
    const viewEquipmentDetail = (equipment) => {
      selectedEquipment.value = equipment
      showDetailModal.value = true
    }
    
    const closeDetailModal = () => {
      showDetailModal.value = false
      selectedEquipment.value = {}
    }
    
    const handleImageError = (event) => {
      event.target.src = '/source/default-equipment.jpg'
    }
    
    // 搜索建议相关方法
    const filterSuggestions = () => {
      if (!searchKeyword.value.trim()) {
        filteredSuggestions.value = searchSuggestions.value.slice(0, 8)
      } else {
        filteredSuggestions.value = searchSuggestions.value
          .filter(suggestion => 
            suggestion.toLowerCase().includes(searchKeyword.value.toLowerCase())
          )
          .slice(0, 8)
      }
    }
    
    const selectSuggestion = (suggestion) => {
      searchKeyword.value = suggestion
      showSearchSuggestions.value = false
      searchEquipment()
    }
    
    const hideSearchSuggestions = () => {
      setTimeout(() => {
        showSearchSuggestions.value = false
      }, 200) // 延迟隐藏，允许点击建议项
    }
    
    // 生命周期
    onMounted(() => {
      loadCategories()
      searchEquipment()
      filterSuggestions() // 初始化建议列表
    })
    
    return {
      loading,
      searchKeyword,
      selectedCategory,
      priceRange,
      selectedPlatform,
      sortBy,
      currentPage,
      totalPages,
      categories,
      equipmentList,
      showDetailModal,
      selectedEquipment,
      searchEquipment,
      changePage,
      viewEquipmentDetail,
      closeDetailModal,
      handleImageError,
      // 搜索建议相关
      showSearchSuggestions,
      filteredSuggestions,
      filterSuggestions,
      selectSuggestion,
      hideSearchSuggestions
    }
  }
}
</script>

<style scoped>
.equipment-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9));
  padding: 100px 0 60px;
  text-align: center;
  color: white;
}

.hero-content h1 {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 20px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.hero-content p {
  font-size: 1.2rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* 搜索和筛选区域 */
.search-section {
  background: white;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 40px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.search-bar {
  margin-bottom: 25px;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: #f8f9fa;
  border-radius: 8px;
  padding: 0 15px;
  border: 2px solid transparent;
  transition: border-color 0.3s;
}

.search-input-wrapper:focus-within {
  border-color: #667eea;
}

.search-input-wrapper i {
  color: #6c757d;
  margin-right: 10px;
}

.search-input-wrapper input {
  flex: 1;
  border: none;
  background: none;
  padding: 15px 0;
  font-size: 1rem;
  outline: none;
}

/* 搜索建议下拉菜单样式 */
.search-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 1000;
  max-height: 300px;
  overflow-y: auto;
}

.suggestions-header {
  padding: 12px 16px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  font-size: 0.9rem;
  color: #6c757d;
  font-weight: 600;
}

.suggestions-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.suggestion-item {
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  border-bottom: 1px solid #f8f9fa;
}

.suggestion-item:hover {
  background-color: #f8f9fa;
}

.suggestion-item:last-child {
  border-bottom: none;
}

.no-suggestions {
  padding: 16px;
  text-align: center;
  color: #6c757d;
  font-style: italic;
}

.search-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.search-btn:hover {
  transform: translateY(-2px);
}

.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  font-weight: 600;
  color: #495057;
  font-size: 0.9rem;
}

.filter-group select {
  padding: 10px;
  border: 2px solid #e9ecef;
  border-radius: 6px;
  font-size: 1rem;
  background: white;
  transition: border-color 0.3s;
}

.filter-group select:focus {
  outline: none;
  border-color: #667eea;
}

/* 装备列表区域 */
.equipment-section {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f8f9fa;
}

.section-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 10px;
}

.sort-options label {
  font-weight: 600;
  color: #495057;
}

.sort-options select {
  padding: 8px 12px;
  border: 2px solid #e9ecef;
  border-radius: 6px;
  background: white;
}

/* 加载状态 */
.loading {
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
}

.loading i {
  font-size: 2rem;
  margin-bottom: 15px;
  color: #667eea;
}

.loading p {
  font-size: 1.1rem;
}

/* 装备网格 */
.equipment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.equipment-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid transparent;
}

.equipment-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
  border-color: #667eea;
}

.equipment-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.equipment-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.equipment-card:hover .equipment-image img {
  transform: scale(1.05);
}

.equipment-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  color: white;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 5px;
}

.equipment-content {
  padding: 20px;
}

.equipment-header {
  margin-bottom: 15px;
}

.equipment-header h3 {
  font-size: 1.2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 5px 0;
  line-height: 1.3;
}

.brand {
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 500;
}

.equipment-rating {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.stars {
  display: flex;
  gap: 2px;
}

.stars i {
  color: #ddd;
  font-size: 0.9rem;
}

.stars i.active {
  color: #ffc107;
}

.rating-text {
  font-size: 0.9rem;
  color: #6c757d;
}

.equipment-description {
  margin-bottom: 15px;
}

.equipment-description p {
  color: #6c757d;
  font-size: 0.9rem;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.equipment-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
}

.current-price {
  font-size: 1.3rem;
  font-weight: 700;
  color: #e74c3c;
}

.platform {
  font-size: 0.9rem;
  color: #6c757d;
  background: white;
  padding: 4px 8px;
  border-radius: 4px;
}

.equipment-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background: #e9ecef;
  color: #495057;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 20px;
  color: #dee2e6;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #495057;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 40px;
}

.page-btn {
  background: #f8f9fa;
  border: 2px solid #dee2e6;
  color: #495057;
  padding: 10px 15px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-weight: 600;
  color: #495057;
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  border-bottom: 2px solid #f8f9fa;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6c757d;
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
  transition: background 0.3s;
}

.close-btn:hover {
  background: #f8f9fa;
}

.modal-body {
  padding: 30px;
}

.equipment-detail {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.detail-images img {
  width: 100%;
  border-radius: 8px;
}

.detail-info h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 1.2rem;
  border-bottom: 2px solid #f8f9fa;
  padding-bottom: 8px;
}

.basic-info,
.specifications,
.description,
.price-info {
  margin-bottom: 25px;
}

.info-item,
.spec-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f8f9fa;
}

.info-item:last-child,
.spec-item:last-child {
  border-bottom: none;
}

.info-item label,
.spec-item label {
  font-weight: 600;
  color: #495057;
  min-width: 80px;
}

.spec-grid {
  display: grid;
  gap: 8px;
}

.description p {
  color: #6c757d;
  line-height: 1.6;
  margin: 0;
}

.price-display {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
}

.price-display .price {
  font-size: 1.8rem;
  font-weight: 700;
  color: #e74c3c;
}

.price-display .platform {
  background: #f8f9fa;
  padding: 6px 12px;
  border-radius: 6px;
  color: #495057;
  font-weight: 500;
}

.buy-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  text-decoration: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 600;
  transition: transform 0.2s;
}

.buy-btn:hover {
  transform: translateY(-2px);
  text-decoration: none;
  color: white;
}

/* 数据分析区域样式 */
.analytics-section {
  margin-top: 40px;
  padding: 30px 0;
  background: #f8f9fa;
  border-radius: 12px;
}

.analytics-section .section-header {
  text-align: center;
  margin-bottom: 30px;
}

.analytics-section .section-header h2 {
  color: #333;
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 10px;
}

.analytics-section .section-header p {
  color: #666;
  font-size: 16px;
  margin: 0;
}

.analytics-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 0 20px;
}

.analytics-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.analytics-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.analytics-card.full-width {
  width: 100%;
}

.analytics-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .container {
    padding: 20px 15px;
  }
  
  .search-section,
  .equipment-section {
    padding: 20px;
  }
  
  .filters {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .equipment-grid {
    grid-template-columns: 1fr;
  }
  
  .equipment-detail {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    margin: 10px;
    max-height: calc(100vh - 20px);
  }
  
  .modal-header,
  .modal-body {
    padding: 20px;
  }
  
  /* 数据分析区域响应式 */
  .analytics-section {
    margin-top: 30px;
    padding: 20px 0;
  }
  
  .analytics-section .section-header h2 {
    font-size: 24px;
  }
  
  .analytics-grid {
    padding: 0 15px;
  }
  
  .analytics-row {
    grid-template-columns: 1fr;
  }
}
</style>