<template>
  <div class="price-distribution-chart">
    <div class="chart-header">
      <h3>{{ title }}</h3>
      <div class="chart-controls">
        <select v-model="selectedCategory" @change="loadDistributionData">
          <option value="all">全部分类</option>
          <option value="helmet">骑行头盔</option>
          <option value="bike">自行车</option>
          <option value="clothing">骑行服装</option>
          <option value="accessories">配件</option>
        </select>
      </div>
    </div>
    <div v-if="loading" class="chart-loading">加载中...</div>
    <div v-else class="chart-container">
      <Bar :data="chartData" :options="chartOptions" :key="chartKey" />
    </div>
    <div class="chart-summary">
      <div class="summary-stats">
        <div class="stat-card">
          <div class="stat-label">平均价格</div>
          <div class="stat-value">¥{{ averagePrice }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">最热门价格区间</div>
          <div class="stat-value">{{ mostPopularRange }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">总产品数</div>
          <div class="stat-value">{{ totalProducts }}款</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { Bar } from 'vue-chartjs'
import { ref, computed, onMounted, watch } from 'vue'
import ApiService from '@/services/api.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const MOCK_DATA = {
  all: { ranges: [
    { label: '0-100', count: 45, percentage: 12 }, { label: '100-500', count: 89, percentage: 24 },
    { label: '500-1000', count: 76, percentage: 20 }, { label: '1000-2000', count: 67, percentage: 18 },
    { label: '2000-5000', count: 54, percentage: 14 }, { label: '5000+', count: 12, percentage: 3 }
  ], averagePrice: 1245, totalProducts: 375 },
  helmet: { ranges: [
    { label: '0-100', count: 23, percentage: 18 }, { label: '100-500', count: 45, percentage: 35 },
    { label: '500-1000', count: 32, percentage: 25 }, { label: '1000-2000', count: 18, percentage: 14 },
    { label: '2000-5000', count: 8, percentage: 6 }, { label: '5000+', count: 0, percentage: 0 }
  ], averagePrice: 385, totalProducts: 129 },
  bike: { ranges: [
    { label: '0-100', count: 0, percentage: 0 }, { label: '100-500', count: 2, percentage: 2 },
    { label: '500-1000', count: 12, percentage: 12 }, { label: '1000-2000', count: 28, percentage: 28 },
    { label: '2000-5000', count: 35, percentage: 35 }, { label: '5000+', count: 18, percentage: 18 }
  ], averagePrice: 3850, totalProducts: 100 },
  clothing: { ranges: [
    { label: '0-100', count: 15, percentage: 20 }, { label: '100-500', count: 28, percentage: 37 },
    { label: '500-1000', count: 18, percentage: 24 }, { label: '1000-2000', count: 10, percentage: 13 },
    { label: '2000-5000', count: 4, percentage: 5 }, { label: '5000+', count: 0, percentage: 0 }
  ], averagePrice: 320, totalProducts: 76 },
  accessories: { ranges: [
    { label: '0-100', count: 32, percentage: 46 }, { label: '100-500', count: 22, percentage: 31 },
    { label: '500-1000', count: 8, percentage: 11 }, { label: '1000-2000', count: 5, percentage: 7 },
    { label: '2000-5000', count: 3, percentage: 4 }, { label: '5000+', count: 0, percentage: 0 }
  ], averagePrice: 185, totalProducts: 71 }
}

export default {
  name: 'PriceDistributionChart',
  components: { Bar },
  props: {
    title: { type: String, default: '价格分布统计' },
    categoryId: { type: [String, Number], default: 'all' }
  },
  setup(props) {
    const selectedCategory = ref(props.categoryId || 'all')
    const chartKey = ref(0)
    const loading = ref(false)
    const liveData = ref(null)

    const distributionData = computed(() => liveData.value || MOCK_DATA[selectedCategory.value] || MOCK_DATA.all)
    const averagePrice = computed(() => (distributionData.value.averagePrice || 0).toLocaleString())
    const totalProducts = computed(() => distributionData.value.totalProducts || 0)
    const mostPopularRange = computed(() => {
      const ranges = distributionData.value.ranges || []
      if (!ranges.length) return '-'
      const max = ranges.reduce((a, b) => b.count > a.count ? b : a)
      return `¥${max.label}`
    })

    const COLORS = ['rgba(54,162,235,0.8)','rgba(255,99,132,0.8)','rgba(255,206,86,0.8)','rgba(75,192,192,0.8)','rgba(153,102,255,0.8)','rgba(255,159,64,0.8)']
    const BORDERS = ['rgba(54,162,235,1)','rgba(255,99,132,1)','rgba(255,206,86,1)','rgba(75,192,192,1)','rgba(153,102,255,1)','rgba(255,159,64,1)']

    const chartData = computed(() => {
      const ranges = distributionData.value.ranges || []
      return {
        labels: ranges.map(r => `¥${r.label}`),
        datasets: [{
          label: '产品数量',
          data: ranges.map(r => r.count),
          backgroundColor: ranges.map((_, i) => COLORS[i % COLORS.length]),
          borderColor: ranges.map((_, i) => BORDERS[i % BORDERS.length]),
          borderWidth: 2, borderRadius: 4, borderSkipped: false
        }]
      }
    })

    const chartOptions = {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (ctx) => { const r = (distributionData.value.ranges || [])[ctx.dataIndex]; return r ? `${r.count}款产品 (${r.percentage}%)` : '' } } }
      },
      scales: {
        x: { display: true, title: { display: true, text: '价格区间' }, grid: { display: false } },
        y: { display: true, title: { display: true, text: '产品数量' }, beginAtZero: true, grid: { color: 'rgba(0,0,0,0.1)' } }
      }
    }

    const loadDistributionData = async () => {
      loading.value = true
      try {
        const cat = selectedCategory.value !== 'all' ? selectedCategory.value : null
        const res = await ApiService.analysis.getPriceDistribution(cat)
        if (res && res.success && res.data && res.data.ranges && res.data.ranges.length) {
          liveData.value = res.data
        } else {
          liveData.value = null
        }
      } catch {
        liveData.value = null
      } finally {
        loading.value = false
        chartKey.value++
      }
    }

    onMounted(loadDistributionData)
    watch(selectedCategory, loadDistributionData)

    return { selectedCategory, chartKey, loading, chartData, chartOptions, averagePrice, totalProducts, mostPopularRange, loadDistributionData }
  }
}
</script>

<style scoped>
.price-distribution-chart { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
.chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.chart-header h3 { margin: 0; color: #333; font-size: 18px; font-weight: 600; }
.chart-controls select { padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; background: white; font-size: 14px; cursor: pointer; }
.chart-loading { height: 350px; display: flex; align-items: center; justify-content: center; color: #999; font-size: 14px; }
.chart-container { height: 350px; margin-bottom: 20px; }
.summary-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }
.stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; transition: transform 0.3s ease; }
.stat-card:hover { transform: translateY(-3px); }
.stat-card:nth-child(2) { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.stat-card:nth-child(3) { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.stat-label { font-size: 12px; opacity: 0.9; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
.stat-value { font-size: 20px; font-weight: 700; margin: 0; }
@media (max-width: 768px) { .chart-header { flex-direction: column; gap: 15px; align-items: flex-start; } .summary-stats { grid-template-columns: 1fr; } .chart-container { height: 300px; } }
</style>