content = r'''<template>
  <div class="price-history-chart">
    <div class="chart-header">
      <h3>{{ title }}</h3>
      <div class="chart-controls">
        <select v-model="selectedTimeRange" @change="loadPriceData">
          <option value="7">近7天</option>
          <option value="30">近30天</option>
          <option value="90">近90天</option>
          <option value="180">近180天</option>
        </select>
      </div>
    </div>
    <div v-if="loading" style="height:300px;display:flex;align-items:center;justify-content:center;color:#999">加载中...</div>
    <div v-else class="chart-container">
      <Line :data="chartData" :options="chartOptions" :key="chartKey" />
    </div>
    <div class="chart-legend">
      <div v-for="platform in platforms" :key="platform.name" class="legend-item">
        <div class="legend-color" :style="{ backgroundColor: platform.color }"></div>
        <span class="legend-label">{{ platform.name }}</span>
        <span class="legend-price">¥{{ platform.currentPrice }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js'
import { Line } from 'vue-chartjs'
import { ref, computed, onMounted, watch } from 'vue'
import ApiService from '@/services/api.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const PLATFORM_COLORS = {
  'TMall': { border: '#ff6900', bg: 'rgba(255,105,0,0.1)' },
  'JD': { border: '#e1251b', bg: 'rgba(225,37,27,0.1)' },
  'Taobao': { border: '#ff4400', bg: 'rgba(255,68,0,0.1)' },
  '\u5929\u732b': { border: '#ff6900', bg: 'rgba(255,105,0,0.1)' },
  '\u4eac\u4e1c': { border: '#e1251b', bg: 'rgba(225,37,27,0.1)' },
  '\u6de1\u5b9d': { border: '#ff4400', bg: 'rgba(255,68,0,0.1)' },
}

function getColor(name) {
  return PLATFORM_COLORS[name] || { border: '#888', bg: 'rgba(136,136,136,0.1)' }
}

function buildMockData(days) {
  const n = days <= 7 ? 7 : days <= 30 ? 30 : 18
  const step = days <= 30 ? 1 : Math.ceil(days / 18)
  const labels = Array.from({ length: n }, (_, i) => {
    const d = new Date(); d.setDate(d.getDate() - (n - 1 - i) * step)
    return (d.getMonth() + 1) + '-' + String(d.getDate()).padStart(2, '0')
  })
  const platforms = ['\u5929\u732b', '\u4eac\u4e1c', '\u6de1\u5b9d']
  const base = [1300, 1320, 1280]
  const datasets = {}
  platforms.forEach((p, idx) => {
    datasets[p] = labels.map((_, i) => Math.round(base[idx] - i * 2 + (Math.random() * 20 - 10)))
  })
  return { labels, datasets }
}

export default {
  name: 'PriceHistoryChart',
  components: { Line },
  props: {
    title: { type: String, default: '\u4ef7\u683c\u5386\u53f2\u8d8b\u52bf' },
    equipmentId: { type: [String, Number], required: true }
  },
  setup(props) {
    const selectedTimeRange = ref('30')
    const chartKey = ref(0)
    const loading = ref(false)
    const liveLabels = ref([])
    const liveDatasets = ref({})

    const platforms = computed(() => {
      const dsMap = liveLabels.value.length ? liveDatasets.value : buildMockData(Number(selectedTimeRange.value)).datasets
      return Object.entries(dsMap).map(([name, prices]) => ({
        name, color: getColor(name).border,
        currentPrice: Array.isArray(prices) ? Math.round(prices.filter(Boolean).slice(-1)[0] || 0) : 0
      }))
    })

    const chartData = computed(() => {
      let labels, dsMap
      if (liveLabels.value.length) { labels = liveLabels.value; dsMap = liveDatasets.value }
      else { const m = buildMockData(Number(selectedTimeRange.value)); labels = m.labels; dsMap = m.datasets }
      return {
        labels,
        datasets: Object.entries(dsMap).map(([name, data]) => ({
          label: name,
          data: data.map(v => v !== null && v !== undefined ? Math.round(v) : null),
          borderColor: getColor(name).border,
          backgroundColor: getColor(name).bg,
          tension: 0.4, fill: false, pointRadius: 3, pointHoverRadius: 6, spanGaps: true
        }))
      }
    })

    const chartOptions = {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { mode: 'index', intersect: false, callbacks: { label: ctx => ctx.dataset.label + ': \xa5' + ctx.parsed.y } } },
      scales: {
        x: { display: true, title: { display: true, text: '\u65e5\u671f' }, grid: { display: false } },
        y: { display: true, title: { display: true, text: '\u4ef7\u683c (\xa5)' }, grid: { color: 'rgba(0,0,0,0.1)' } }
      },
      interaction: { mode: 'nearest', axis: 'x', intersect: false }
    }

    const updateChart = () => { chartKey.value++ }

    const loadPriceData = async () => {
      if (!props.equipmentId) return
      loading.value = true
      try {
        const res = await ApiService.analysis.getPriceHistory(props.equipmentId, Number(selectedTimeRange.value))
        if (res && res.success && res.data && res.data.labels && res.data.labels.length) {
          liveLabels.value = res.data.labels; liveDatasets.value = res.data.datasets
        } else { liveLabels.value = []; liveDatasets.value = {} }
      } catch { liveLabels.value = []; liveDatasets.value = {} }
      finally { loading.value = false; updateChart() }
    }

    onMounted(loadPriceData)
    watch(() => props.equipmentId, loadPriceData)
    watch(selectedTimeRange, loadPriceData)

    return { selectedTimeRange, chartKey, chartData, chartOptions, platforms, loading, updateChart }
  }
}
</script>

<style scoped>
.price-history-chart { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
.chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.chart-header h3 { margin: 0; color: #333; font-size: 18px; font-weight: 600; }
.chart-controls select { padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; background: white; font-size: 14px; cursor: pointer; }
.chart-container { height: 300px; margin-bottom: 20px; }
.chart-legend { display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; }
.legend-item { display: flex; align-items: center; gap: 8px; }
.legend-color { width: 12px; height: 12px; border-radius: 50%; }
.legend-label { font-size: 14px; color: #666; }
.legend-price { font-size: 14px; font-weight: 600; color: #333; }
@media (max-width: 768px) { .chart-header { flex-direction: column; gap: 15px; align-items: flex-start; } .chart-legend { gap: 15px; } .chart-container { height: 250px; } }
</style>
'''

with open('src/components/PriceHistoryChart.vue', 'w', encoding='utf-8') as f:
    f.write(content)
print('PriceHistoryChart.vue written OK')
