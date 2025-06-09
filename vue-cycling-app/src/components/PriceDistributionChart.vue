<template>
  <div class="price-distribution-chart">
    <div class="chart-header">
      <h3>{{ title }}</h3>
      <div class="chart-controls">
        <select v-model="selectedCategory" @change="updateChart">
          <option value="all">全部分类</option>
          <option value="helmet">骑行头盔</option>
          <option value="bike">自行车</option>
          <option value="clothing">骑行服装</option>
          <option value="accessories">配件</option>
        </select>
      </div>
    </div>
    <div class="chart-container">
      <Bar
        :data="chartData"
        :options="chartOptions"
        :key="chartKey"
      />
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
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Bar } from 'vue-chartjs'
import { ref, computed, onMounted, watch } from 'vue'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

export default {
  name: 'PriceDistributionChart',
  components: {
    Bar
  },
  props: {
    title: {
      type: String,
      default: '价格分布统计'
    },
    categoryId: {
      type: [String, Number],
      default: 'all'
    }
  },
  setup(props) {
    const selectedCategory = ref(props.categoryId || 'all')
    const chartKey = ref(0)
    
    // 模拟数据 - 实际项目中应该从API获取
    const mockDistributionData = {
      all: {
        ranges: [
          { label: '0-100', min: 0, max: 100, count: 45, percentage: 12 },
          { label: '100-300', min: 100, max: 300, count: 89, percentage: 24 },
          { label: '300-500', min: 300, max: 500, count: 76, percentage: 20 },
          { label: '500-1000', min: 500, max: 1000, count: 67, percentage: 18 },
          { label: '1000-2000', min: 1000, max: 2000, count: 54, percentage: 14 },
          { label: '2000-5000', min: 2000, max: 5000, count: 32, percentage: 9 },
          { label: '5000+', min: 5000, max: null, count: 12, percentage: 3 }
        ],
        averagePrice: 1245,
        totalProducts: 375
      },
      helmet: {
        ranges: [
          { label: '0-100', min: 0, max: 100, count: 23, percentage: 18 },
          { label: '100-300', min: 100, max: 300, count: 45, percentage: 35 },
          { label: '300-500', min: 300, max: 500, count: 32, percentage: 25 },
          { label: '500-1000', min: 500, max: 1000, count: 18, percentage: 14 },
          { label: '1000-2000', min: 1000, max: 2000, count: 8, percentage: 6 },
          { label: '2000-5000', min: 2000, max: 5000, count: 3, percentage: 2 },
          { label: '5000+', min: 5000, max: null, count: 0, percentage: 0 }
        ],
        averagePrice: 385,
        totalProducts: 129
      },
      bike: {
        ranges: [
          { label: '0-100', min: 0, max: 100, count: 0, percentage: 0 },
          { label: '100-300', min: 100, max: 300, count: 2, percentage: 2 },
          { label: '300-500', min: 300, max: 500, count: 5, percentage: 5 },
          { label: '500-1000', min: 500, max: 1000, count: 12, percentage: 12 },
          { label: '1000-2000', min: 1000, max: 2000, count: 28, percentage: 28 },
          { label: '2000-5000', min: 2000, max: 5000, count: 35, percentage: 35 },
          { label: '5000+', min: 5000, max: null, count: 18, percentage: 18 }
        ],
        averagePrice: 3850,
        totalProducts: 100
      },
      clothing: {
        ranges: [
          { label: '0-100', min: 0, max: 100, count: 15, percentage: 20 },
          { label: '100-300', min: 100, max: 300, count: 28, percentage: 37 },
          { label: '300-500', min: 300, max: 500, count: 18, percentage: 24 },
          { label: '500-1000', min: 500, max: 1000, count: 10, percentage: 13 },
          { label: '1000-2000', min: 1000, max: 2000, count: 4, percentage: 5 },
          { label: '2000-5000', min: 2000, max: 5000, count: 1, percentage: 1 },
          { label: '5000+', min: 5000, max: null, count: 0, percentage: 0 }
        ],
        averagePrice: 320,
        totalProducts: 76
      },
      accessories: {
        ranges: [
          { label: '0-100', min: 0, max: 100, count: 32, percentage: 46 },
          { label: '100-300', min: 100, max: 300, count: 22, percentage: 31 },
          { label: '300-500', min: 300, max: 500, count: 8, percentage: 11 },
          { label: '500-1000', min: 500, max: 1000, count: 5, percentage: 7 },
          { label: '1000-2000', min: 1000, max: 2000, count: 3, percentage: 4 },
          { label: '2000-5000', min: 2000, max: 5000, count: 1, percentage: 1 },
          { label: '5000+', min: 5000, max: null, count: 0, percentage: 0 }
        ],
        averagePrice: 185,
        totalProducts: 71
      }
    }
    
    const distributionData = computed(() => {
      return mockDistributionData[selectedCategory.value] || mockDistributionData.all
    })
    
    const averagePrice = computed(() => {
      return distributionData.value.averagePrice.toLocaleString()
    })
    
    const totalProducts = computed(() => {
      return distributionData.value.totalProducts
    })
    
    const mostPopularRange = computed(() => {
      const ranges = distributionData.value.ranges
      const maxRange = ranges.reduce((max, range) => 
        range.count > max.count ? range : max
      )
      return `¥${maxRange.label}`
    })
    
    const chartData = computed(() => {
      const ranges = distributionData.value.ranges
      return {
        labels: ranges.map(range => `¥${range.label}`),
        datasets: [
          {
            label: '产品数量',
            data: ranges.map(range => range.count),
            backgroundColor: ranges.map((range, index) => {
              const colors = [
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 99, 132, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(255, 159, 64, 0.8)',
                'rgba(199, 199, 199, 0.8)'
              ]
              return colors[index % colors.length]
            }),
            borderColor: ranges.map((range, index) => {
              const colors = [
                'rgba(54, 162, 235, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(199, 199, 199, 1)'
              ]
              return colors[index % colors.length]
            }),
            borderWidth: 2,
            borderRadius: 4,
            borderSkipped: false
          }
        ]
      }
    })
    
    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const range = distributionData.value.ranges[context.dataIndex]
              return `${range.count}款产品 (${range.percentage}%)`
            }
          }
        }
      },
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: '价格区间'
          },
          grid: {
            display: false
          }
        },
        y: {
          display: true,
          title: {
            display: true,
            text: '产品数量'
          },
          beginAtZero: true,
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          }
        }
      }
    }
    
    const updateChart = () => {
      chartKey.value++
    }
    
    const loadDistributionData = async () => {
      // 实际项目中这里应该调用API获取真实数据
      // const response = await ApiService.equipment.getPriceDistribution(selectedCategory.value)
      // distributionData.value = response.data
    }
    
    onMounted(() => {
      loadDistributionData()
    })
    
    watch(selectedCategory, () => {
      loadDistributionData()
      updateChart()
    })
    
    return {
      selectedCategory,
      chartKey,
      chartData,
      chartOptions,
      averagePrice,
      totalProducts,
      mostPopularRange,
      updateChart
    }
  }
}
</script>

<style scoped>
.price-distribution-chart {
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
  height: 350px;
  margin-bottom: 20px;
}

.chart-summary {
  margin-top: 20px;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
}

.stat-card:nth-child(2) {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-card:nth-child(3) {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-label {
  font-size: 12px;
  opacity: 0.9;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  margin: 0;
}

@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .summary-stats {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 300px;
  }
}
</style>