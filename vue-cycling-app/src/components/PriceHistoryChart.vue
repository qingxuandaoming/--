<template>
  <div class="price-history-chart">
    <div class="chart-header">
      <h3>{{ title }}</h3>
      <div class="chart-controls">
        <select v-model="selectedTimeRange" @change="updateChart">
          <option value="7">近7天</option>
          <option value="30">近30天</option>
          <option value="90">近3个月</option>
          <option value="180">近6个月</option>
        </select>
      </div>
    </div>
    <div class="chart-container">
      <Line
        :data="chartData"
        :options="chartOptions"
        :key="chartKey"
      />
    </div>
    <div class="chart-legend">
      <div class="legend-item" v-for="platform in platforms" :key="platform.name">
        <span class="legend-color" :style="{ backgroundColor: platform.color }"></span>
        <span class="legend-label">{{ platform.name }}</span>
        <span class="legend-price">¥{{ platform.currentPrice }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line } from 'vue-chartjs'
import { ref, computed, onMounted, watch } from 'vue'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

export default {
  name: 'PriceHistoryChart',
  components: {
    Line
  },
  props: {
    title: {
      type: String,
      default: '价格历史趋势'
    },
    equipmentId: {
      type: [String, Number],
      required: true
    }
  },
  setup(props) {
    const selectedTimeRange = ref('30')
    const chartKey = ref(0)
    const priceData = ref({})
    
    // 模拟数据 - 实际项目中应该从API获取
    const mockPriceData = {
      '7': {
        labels: ['12-01', '12-02', '12-03', '12-04', '12-05', '12-06', '12-07'],
        datasets: {
          '天猫': [1299, 1289, 1279, 1269, 1259, 1249, 1239],
          '京东': [1319, 1309, 1299, 1289, 1279, 1269, 1259],
          '淘宝': [1279, 1269, 1259, 1249, 1239, 1229, 1219]
        }
      },
      '30': {
        labels: Array.from({length: 30}, (_, i) => {
          const date = new Date()
          date.setDate(date.getDate() - 29 + i)
          return `${date.getMonth() + 1}-${date.getDate().toString().padStart(2, '0')}`
        }),
        datasets: {
          '天猫': Array.from({length: 30}, (_, i) => 1300 - i * 2 + Math.random() * 20 - 10),
          '京东': Array.from({length: 30}, (_, i) => 1320 - i * 2.5 + Math.random() * 25 - 12),
          '淘宝': Array.from({length: 30}, (_, i) => 1280 - i * 1.8 + Math.random() * 18 - 9)
        }
      },
      '90': {
        labels: Array.from({length: 18}, (_, i) => {
          const date = new Date()
          date.setDate(date.getDate() - 90 + i * 5)
          return `${date.getMonth() + 1}-${date.getDate().toString().padStart(2, '0')}`
        }),
        datasets: {
          '天猫': Array.from({length: 18}, (_, i) => 1400 - i * 8 + Math.random() * 40 - 20),
          '京东': Array.from({length: 18}, (_, i) => 1420 - i * 9 + Math.random() * 45 - 22),
          '淘宝': Array.from({length: 18}, (_, i) => 1380 - i * 7 + Math.random() * 35 - 17)
        }
      },
      '180': {
        labels: Array.from({length: 18}, (_, i) => {
          const date = new Date()
          date.setDate(date.getDate() - 180 + i * 10)
          return `${date.getMonth() + 1}-${date.getDate().toString().padStart(2, '0')}`
        }),
        datasets: {
          '天猫': Array.from({length: 18}, (_, i) => 1500 - i * 12 + Math.random() * 60 - 30),
          '京东': Array.from({length: 18}, (_, i) => 1520 - i * 13 + Math.random() * 65 - 32),
          '淘宝': Array.from({length: 18}, (_, i) => 1480 - i * 11 + Math.random() * 55 - 27)
        }
      }
    }
    
    const platforms = computed(() => {
      const currentData = mockPriceData[selectedTimeRange.value]
      if (!currentData) return []
      
      return [
        {
          name: '天猫',
          color: '#ff6900',
          currentPrice: Math.round(currentData.datasets['天猫'][currentData.datasets['天猫'].length - 1])
        },
        {
          name: '京东',
          color: '#e1251b',
          currentPrice: Math.round(currentData.datasets['京东'][currentData.datasets['京东'].length - 1])
        },
        {
          name: '淘宝',
          color: '#ff4400',
          currentPrice: Math.round(currentData.datasets['淘宝'][currentData.datasets['淘宝'].length - 1])
        }
      ]
    })
    
    const chartData = computed(() => {
      const currentData = mockPriceData[selectedTimeRange.value]
      if (!currentData) return { labels: [], datasets: [] }
      
      return {
        labels: currentData.labels,
        datasets: [
          {
            label: '天猫',
            data: currentData.datasets['天猫'].map(price => Math.round(price)),
            borderColor: '#ff6900',
            backgroundColor: 'rgba(255, 105, 0, 0.1)',
            tension: 0.4,
            fill: false,
            pointRadius: 3,
            pointHoverRadius: 6
          },
          {
            label: '京东',
            data: currentData.datasets['京东'].map(price => Math.round(price)),
            borderColor: '#e1251b',
            backgroundColor: 'rgba(225, 37, 27, 0.1)',
            tension: 0.4,
            fill: false,
            pointRadius: 3,
            pointHoverRadius: 6
          },
          {
            label: '淘宝',
            data: currentData.datasets['淘宝'].map(price => Math.round(price)),
            borderColor: '#ff4400',
            backgroundColor: 'rgba(255, 68, 0, 0.1)',
            tension: 0.4,
            fill: false,
            pointRadius: 3,
            pointHoverRadius: 6
          }
        ]
      }
    })
    
    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: false
        },
        legend: {
          display: false
        },
        tooltip: {
          mode: 'index',
          intersect: false,
          callbacks: {
            label: function(context) {
              return `${context.dataset.label}: ¥${context.parsed.y}`
            }
          }
        }
      },
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: '日期'
          },
          grid: {
            display: false
          }
        },
        y: {
          display: true,
          title: {
            display: true,
            text: '价格 (¥)'
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          }
        }
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false
      }
    }
    
    const updateChart = () => {
      chartKey.value++
    }
    
    const loadPriceData = async () => {
      // 实际项目中这里应该调用API获取真实数据
      // const response = await ApiService.equipment.getPriceHistory(props.equipmentId, selectedTimeRange.value)
      // priceData.value = response.data
    }
    
    onMounted(() => {
      loadPriceData()
    })
    
    watch(selectedTimeRange, () => {
      loadPriceData()
    })
    
    return {
      selectedTimeRange,
      chartKey,
      chartData,
      chartOptions,
      platforms,
      updateChart
    }
  }
}
</script>

<style scoped>
.price-history-chart {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.chart-controls select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  font-size: 14px;
  cursor: pointer;
}

.chart-controls select:focus {
  outline: none;
  border-color: #4CAF50;
}

.chart-container {
  height: 300px;
  margin-bottom: 20px;
}

.chart-legend {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-label {
  font-size: 14px;
  color: #666;
}

.legend-price {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .chart-legend {
    gap: 15px;
  }
  
  .chart-container {
    height: 250px;
  }
}
</style>