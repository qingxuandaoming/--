<template>
  <div class="brand-radar-chart">
    <div class="chart-header">
      <h3>{{ title }}</h3>
      <div class="chart-controls">
        <div class="brand-selector">
          <label>对比品牌:</label>
          <div class="brand-checkboxes">
            <label v-for="brand in availableBrands" :key="brand.id" class="checkbox-label">
              <input 
                type="checkbox" 
                :value="brand.id" 
                v-model="selectedBrands"
                @change="updateChart"
                :disabled="selectedBrands.length >= 4 && !selectedBrands.includes(brand.id)"
              >
              <span class="checkbox-text">{{ brand.name }}</span>
            </label>
          </div>
        </div>
      </div>
    </div>
    <div class="chart-container">
      <Radar
        :data="chartData"
        :options="chartOptions"
        :key="chartKey"
      />
    </div>
    <div class="chart-legend">
      <div class="legend-grid">
        <div class="legend-item" v-for="brand in activeBrands" :key="brand.id">
          <span class="legend-color" :style="{ backgroundColor: brand.color }"></span>
          <span class="legend-label">{{ brand.name }}</span>
          <span class="legend-score">综合: {{ brand.overallScore }}/5</span>
        </div>
      </div>
    </div>
    <div class="dimension-explanation">
      <h4>评分维度说明</h4>
      <div class="dimension-grid">
        <div class="dimension-item" v-for="dimension in dimensions" :key="dimension.key">
          <div class="dimension-name">{{ dimension.name }}</div>
          <div class="dimension-desc">{{ dimension.description }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
} from 'chart.js'
import { Radar } from 'vue-chartjs'
import { ref, computed, onMounted, watch } from 'vue'

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

export default {
  name: 'BrandRadarChart',
  components: {
    Radar
  },
  props: {
    title: {
      type: String,
      default: '品牌综合评分对比'
    },
    category: {
      type: String,
      default: 'helmet'
    }
  },
  setup(props) {
    const selectedBrands = ref(['giant', 'trek', 'specialized'])
    const chartKey = ref(0)
    
    const dimensions = [
      { key: 'quality', name: '产品质量', description: '材料工艺、耐用性等' },
      { key: 'design', name: '设计美观', description: '外观设计、颜色搭配等' },
      { key: 'comfort', name: '舒适度', description: '佩戴舒适性、人体工学等' },
      { key: 'performance', name: '性能表现', description: '功能性、实用性等' },
      { key: 'value', name: '性价比', description: '价格与价值的匹配度' },
      { key: 'service', name: '售后服务', description: '客服质量、保修政策等' }
    ]
    
    const availableBrands = [
      { id: 'giant', name: 'Giant', color: '#FF6384' },
      { id: 'trek', name: 'Trek', color: '#36A2EB' },
      { id: 'specialized', name: 'Specialized', color: '#FFCE56' },
      { id: 'merida', name: '美利达', color: '#4BC0C0' },
      { id: 'xds', name: '喜德盛', color: '#9966FF' },
      { id: 'scott', name: 'Scott', color: '#FF9F40' },
      { id: 'cannondale', name: 'Cannondale', color: '#FF6B6B' },
      { id: 'bianchi', name: 'Bianchi', color: '#4ECDC4' }
    ]
    
    // 模拟数据 - 实际项目中应该从API获取
    const mockBrandScores = {
      giant: {
        quality: 4.2,
        design: 4.0,
        comfort: 4.1,
        performance: 4.3,
        value: 4.5,
        service: 4.0,
        overallScore: 4.2
      },
      trek: {
        quality: 4.5,
        design: 4.4,
        comfort: 4.3,
        performance: 4.6,
        value: 3.8,
        service: 4.2,
        overallScore: 4.3
      },
      specialized: {
        quality: 4.6,
        design: 4.5,
        comfort: 4.4,
        performance: 4.7,
        value: 3.6,
        service: 4.1,
        overallScore: 4.3
      },
      merida: {
        quality: 4.0,
        design: 3.8,
        comfort: 3.9,
        performance: 4.1,
        value: 4.3,
        service: 3.8,
        overallScore: 4.0
      },
      xds: {
        quality: 3.8,
        design: 3.6,
        comfort: 3.7,
        performance: 3.9,
        value: 4.6,
        service: 3.7,
        overallScore: 3.9
      },
      scott: {
        quality: 4.3,
        design: 4.2,
        comfort: 4.0,
        performance: 4.4,
        value: 3.9,
        service: 4.0,
        overallScore: 4.1
      },
      cannondale: {
        quality: 4.4,
        design: 4.3,
        comfort: 4.2,
        performance: 4.5,
        value: 3.7,
        service: 4.1,
        overallScore: 4.2
      },
      bianchi: {
        quality: 4.1,
        design: 4.6,
        comfort: 4.0,
        performance: 4.2,
        value: 3.5,
        service: 3.9,
        overallScore: 4.1
      }
    }
    
    const activeBrands = computed(() => {
      return selectedBrands.value.map(brandId => {
        const brand = availableBrands.find(b => b.id === brandId)
        const scores = mockBrandScores[brandId]
        return {
          ...brand,
          ...scores
        }
      })
    })
    
    const chartData = computed(() => {
      return {
        labels: dimensions.map(d => d.name),
        datasets: activeBrands.value.map(brand => ({
          label: brand.name,
          data: dimensions.map(d => brand[d.key]),
          borderColor: brand.color,
          backgroundColor: brand.color + '20',
          pointBackgroundColor: brand.color,
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: brand.color,
          pointRadius: 4,
          pointHoverRadius: 6,
          borderWidth: 2
        }))
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
              return `${context.dataset.label}: ${context.parsed.r.toFixed(1)}/5`
            }
          }
        }
      },
      scales: {
        r: {
          beginAtZero: true,
          min: 0,
          max: 5,
          ticks: {
            stepSize: 1,
            callback: function(value) {
              return value.toFixed(1)
            }
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          angleLines: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          pointLabels: {
            font: {
              size: 12
            },
            color: '#333'
          }
        }
      },
      elements: {
        line: {
          tension: 0.1
        }
      }
    }
    
    const updateChart = () => {
      chartKey.value++
    }
    
    const loadBrandScores = async () => {
      // 实际项目中这里应该调用API获取真实数据
      // const response = await ApiService.equipment.getBrandScores(props.category, selectedBrands.value)
      // brandScores.value = response.data
    }
    
    onMounted(() => {
      loadBrandScores()
    })
    
    watch(selectedBrands, () => {
      loadBrandScores()
    }, { deep: true })
    
    return {
      selectedBrands,
      chartKey,
      chartData,
      chartOptions,
      availableBrands,
      activeBrands,
      dimensions,
      updateChart
    }
  }
}
</script>

<style scoped>
.brand-radar-chart {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.chart-header {
  margin-bottom: 20px;
}

.chart-header h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.brand-selector label {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
  display: block;
}

.brand-checkboxes {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.checkbox-label {
  display: flex !important;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 13px !important;
  margin-bottom: 0 !important;
}

.checkbox-label input[type="checkbox"] {
  margin: 0;
}

.checkbox-label input[type="checkbox"]:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.checkbox-text {
  color: #333;
}

.chart-container {
  height: 400px;
  margin-bottom: 20px;
}

.chart-legend {
  margin-bottom: 20px;
}

.legend-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 8px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.legend-label {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  flex: 1;
}

.legend-score {
  font-size: 12px;
  color: #666;
  background: #e9ecef;
  padding: 2px 8px;
  border-radius: 12px;
}

.dimension-explanation {
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.dimension-explanation h4 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
}

.dimension-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}

.dimension-item {
  padding: 12px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 3px solid #4CAF50;
}

.dimension-name {
  font-size: 13px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.dimension-desc {
  font-size: 12px;
  color: #666;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .brand-checkboxes {
    flex-direction: column;
    gap: 10px;
  }
  
  .legend-grid {
    grid-template-columns: 1fr;
  }
  
  .dimension-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 350px;
  }
}
</style>