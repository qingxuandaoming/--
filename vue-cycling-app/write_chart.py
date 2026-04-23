content = '''<template>
  <div class="brand-market-share-chart">
    <div class="chart-header">
      <h3>{{ title }}</h3>
      <div class="chart-controls">
        <select v-model="selectedCategory" @change="loadMarketData">
          <option value="all">全部分类</option>
          <option value="helmet">骑行头盔</option>
          <option value="bike">自行车</option>
          <option value="clothing">骑行服装</option>
          <option value="accessories">配件</option>
        </select>
      </div>
    </div>
    <div v-if="loading" style="height:300px;display:flex;align-items:center;justify-content:center;color:#999">加载中...</div>
    <div v-else class="chart-container">
      <Doughnut :data="chartData" :options="chartOptions" :key="chartKey" />
    </div>
    <div class="chart-stats">
      <div class="stats-grid">
        <div v-for="brand in brandStats" :key="brand.name" class="stat-item">
          <div class="stat-color" :style="{ backgroundColor: brand.color }"></div>
          <div class="stat-info">
            <div class="stat-name">{{ brand.name }}</div>
            <div class="stat-value">{{ brand.percentage }}%</div>
            <div class="stat-count">{{ brand.count }}款产品</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
import { ref, computed, onMounted, watch } from 'vue'
import ApiService from '@/services/api.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const MOCK_DATA = {
  all: { brands: [
    { name: 'Giant', percentage: 22, count: 156, color: '#FF6384' },
    { name: 'Trek', percentage: 18, count: 122, color: '#36A2EB' },
    { name: 'Specialized', percentage: 15, count: 100, color: '#FFCE56' },
    { name: 'Giro', percentage: 12, count: 83, color: '#4BC0C0' },
    { name: 'Garmin', percentage: 10, count: 56, color: '#9966FF' },
    { name: 'Pearl Izumi', percentage: 8, count: 45, color: '#FF9F40' },
    { name: 'Castelli', percentage: 8, count: 40, color: '#FF6B6B' },
    { name: '其他', percentage: 7, count: 39, color: '#4ECDC4' }
  ]},
  helmet: { brands: [
    { name: 'Giro', percentage: 25, count: 45, color: '#FF6384' },
    { name: 'Bell', percentage: 20, count: 36, color: '#36A2EB' },
    { name: 'Specialized', percentage: 18, count: 32, color: '#FFCE56' },
    { name: 'Trek', percentage: 15, count: 27, color: '#4BC0C0' },
    { name: 'Giant', percentage: 12, count: 22, color: '#9966FF' },
    { name: '其他', percentage: 10, count: 18, color: '#FF9F40' }
  ]},
  bike: { brands: [
    { name: 'Giant', percentage: 28, count: 156, color: '#FF6384' },
    { name: 'Trek', percentage: 22, count: 122, color: '#36A2EB' },
    { name: 'Specialized', percentage: 18, count: 100, color: '#FFCE56' },
    { name: 'Merida', percentage: 15, count: 83, color: '#4BC0C0' },
    { name: 'Xidesheng', percentage: 10, count: 56, color: '#9966FF' },
    { name: '其他', percentage: 7, count: 39, color: '#FF9F40' }
  ]},
  clothing: { brands: [
    { name: 'Pearl Izumi', percentage: 22, count: 78, color: '#FF6384' },
    { name: 'Castelli', percentage: 20, count: 71, color: '#36A2EB' },
    { name: 'Rapha', percentage: 18, count: 64, color: '#FFCE56' },
    { name: 'Assos', percentage: 16, count: 57, color: '#4BC0C0' },
    { name: 'Sportful', percentage: 14, count: 50, color: '#9966FF' },
    { name: '其他', percentage: 10, count: 36, color: '#FF9F40' }
  ]},
  accessories: { brands: [
    { name: 'Garmin', percentage: 30, count: 89, color: '#FF6384' },
    { name: 'Wahoo', percentage: 25, count: 74, color: '#36A2EB' },
    { name: 'Cateye', percentage: 20, count: 59, color: '#FFCE56' },
    { name: 'Lezyne', percentage: 15, count: 44, color: '#4BC0C0' },
    { name: 'Topeak', percentage: 7, count: 21, color: '#9966FF' },
    { name: '其他', percentage: 3, count: 9, color: '#FF9F40' }
  ]}
}

export default {
  name: 'BrandMarketShareChart',
  components: { Doughnut },
  props: {
    title: { type: String, default: '品牌市场份额' },
    categoryId: { type: [String, Number], default: 'all' }
  },
  setup(props) {
    const selectedCategory = ref(props.categoryId || 'all')
    const chartKey = ref(0)
    const loading = ref(false)
    const liveBrands = ref([])

    const brandStats = computed(() =>
      liveBrands.value.length ? liveBrands.value : (MOCK_DATA[selectedCategory.value]?.brands || MOCK_DATA.all.brands)
    )

    const chartData = computed(() => {
      const brands = brandStats.value
      return {
        labels: brands.map(b => b.name),
        datasets: [{ data: brands.map(b => b.percentage), backgroundColor: brands.map(b => b.color), borderColor: brands.map(b => b.color), borderWidth: 2, hoverBorderWidth: 3 }]
      }
    })

    const chartOptions = {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (ctx) => { const b = brandStats.value[ctx.dataIndex]; return b ? b.name + ': ' + b.percentage + '% (' + b.count + '款)' : '' } } }
      },
      cutout: '60%',
      elements: { arc: { borderRadius: 4 } }
    }

    const updateChart = () => { chartKey.value++ }

    const loadMarketData = async () => {
      loading.value = true
      try {
        const cat = selectedCategory.value !== 'all' ? selectedCategory.value : null
        const res = await ApiService.analysis.getBrandMarketShare(cat)
        if (res && res.success && res.data && res.data.brands && res.data.brands.length) {
          liveBrands.value = res.data.brands
        } else {
          liveBrands.value = []
        }
      } catch {
        liveBrands.value = []
      } finally {
        loading.value = false
        updateChart()
      }
    }

    onMounted(loadMarketData)
    watch(selectedCategory, loadMarketData)
    watch(() => props.categoryId, (val) => { selectedCategory.value = val || 'all'; loadMarketData() })

    return { selectedCategory, chartKey, chartData, chartOptions, brandStats, loading, updateChart, loadMarketData }
  }
}
</script>

<style scoped>
.brand-market-share-chart { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
.chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.chart-header h3 { margin: 0; color: #333; font-size: 18px; font-weight: 600; }
.chart-controls select { padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; background: white; font-size: 14px; cursor: pointer; }
.chart-container { height: 300px; margin-bottom: 20px; position: relative; }
.chart-stats { margin-top: 20px; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }
.stat-item { display: flex; align-items: center; gap: 12px; padding: 10px; background: #f8f9fa; border-radius: 8px; transition: all 0.3s; }
.stat-item:hover { background: #e9ecef; transform: translateY(-2px); }
.stat-color { width: 16px; height: 16px; border-radius: 50%; flex-shrink: 0; }
.stat-info { flex: 1; }
.stat-name { font-size: 13px; font-weight: 600; color: #333; }
.stat-value { font-size: 15px; font-weight: 700; color: #4CAF50; }
.stat-count { font-size: 11px; color: #666; }
@media (max-width: 768px) { .chart-header { flex-direction: column; gap: 12px; align-items: flex-start; } .stats-grid { grid-template-columns: 1fr; } .chart-container { height: 250px; } }
</style>
'''

with open('src/components/BrandMarketShareChart.vue', 'w', encoding='utf-8') as f:
    f.write(content)
print('BrandMarketShareChart.vue written OK')
