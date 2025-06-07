<template>
  <div class="route-planning-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1><i class="fas fa-route"></i> 智能路线规划</h1>
      <p>基于高德地图API的专业路线规划服务，支持多种交通方式</p>
    </div>

    <!-- 路线规划表单 -->
    <div class="planning-form-section">
      <div class="form-container">
        <h2><i class="fas fa-map-marked-alt"></i> 路线设置</h2>
        
        <form @submit.prevent="planRoute" class="route-form">
          <!-- 起点设置 -->
          <div class="form-group">
            <label for="origin">
              <i class="fas fa-play"></i> 起点
            </label>
            <input 
              type="text" 
              id="origin" 
              v-model="routeForm.origin" 
              placeholder="请输入起点地址，如：石家庄市长安区"
              required
            >
          </div>

          <!-- 终点设置 -->
          <div class="form-group">
            <label for="destination">
              <i class="fas fa-flag-checkered"></i> 终点
            </label>
            <input 
              type="text" 
              id="destination" 
              v-model="routeForm.destination" 
              placeholder="请输入终点地址，如：石家庄市裕华区"
              required
            >
          </div>

          <!-- 途经点设置 -->
          <div class="form-group">
            <label for="waypoints">
              <i class="fas fa-map-pin"></i> 途经点 (可选)
            </label>
            <input 
              type="text" 
              id="waypoints" 
              v-model="routeForm.waypoints" 
              placeholder="多个途经点用分号分隔，如：地点1;地点2"
            >
          </div>

          <!-- 交通方式选择 -->
          <div class="form-group">
            <label for="transportMode">
              <i class="fas fa-car"></i> 交通方式
            </label>
            <select id="transportMode" v-model="routeForm.transportMode" required>
              <option value="driving">🚗 驾车</option>
              <option value="walking">🚶 步行</option>
              <option value="transit">🚌 公交</option>
              <option value="riding">🚴 骑行</option>
            </select>
          </div>

          <!-- 城市设置 -->
          <div class="form-group">
            <label for="city">
              <i class="fas fa-city"></i> 城市
            </label>
            <input 
              type="text" 
              id="city" 
              v-model="routeForm.city" 
              placeholder="请输入城市名称，如：石家庄"
            >
          </div>

          <!-- 路线策略 -->
          <div class="form-group">
            <label for="strategy">
              <i class="fas fa-cogs"></i> 路线策略
            </label>
            <select id="strategy" v-model="routeForm.strategy">
              <option value="0">⚡ 速度优先（时间最短）</option>
              <option value="1">💰 费用优先（费用最少）</option>
              <option value="2">📏 距离优先（距离最短）</option>
              <option value="3">🛣️ 不走快速路</option>
              <option value="4">🚫 不走收费路</option>
              <option value="5">🎯 多策略（综合最优）</option>
            </select>
          </div>

          <!-- 高级选项 -->
          <div class="form-group advanced-options">
            <h3><i class="fas fa-sliders-h"></i> 高级选项</h3>
            
            <div class="checkbox-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="routeForm.returnDetailedInfo">
                <span class="checkmark"></span>
                返回详细路线信息
              </label>
              
              <label class="checkbox-label">
                <input type="checkbox" v-model="routeForm.avoidRestriction">
                <span class="checkmark"></span>
                避开限行区域
              </label>
            </div>

            <div class="form-row" v-if="routeForm.avoidRestriction">
              <div class="form-group half">
                <label for="plateNumber">
                  <i class="fas fa-id-card"></i> 车牌号
                </label>
                <input 
                  type="text" 
                  id="plateNumber" 
                  v-model="routeForm.plateNumber" 
                  placeholder="如：冀A12345"
                >
              </div>
            </div>
          </div>

          <!-- 提交按钮 -->
          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="isLoading">
              <i class="fas fa-route" v-if="!isLoading"></i>
              <i class="fas fa-spinner fa-spin" v-else></i>
              {{ isLoading ? '规划中...' : '开始规划路线' }}
            </button>
            
            <button type="button" class="btn btn-secondary" @click="clearForm">
              <i class="fas fa-eraser"></i>
              清空表单
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 路线结果展示 -->
    <div class="route-result-section" v-if="routeResult">
      <div class="result-container">
        <h2><i class="fas fa-check-circle"></i> 路线规划结果</h2>
        
        <!-- 路线概览 -->
        <div class="route-overview">
          <div class="overview-stats">
            <div class="stat-card">
              <i class="fas fa-route"></i>
              <div class="stat-info">
                <h3>总距离</h3>
                <p>{{ formatDistance(routeResult.distance) }}</p>
              </div>
            </div>
            
            <div class="stat-card">
              <i class="fas fa-clock"></i>
              <div class="stat-info">
                <h3>预计时间</h3>
                <p>{{ formatDuration(routeResult.duration) }}</p>
              </div>
            </div>
            
            <div class="stat-card" v-if="routeResult.tolls">
              <i class="fas fa-coins"></i>
              <div class="stat-info">
                <h3>过路费</h3>
                <p>{{ routeResult.tolls }}元</p>
              </div>
            </div>
            
            <div class="stat-card" v-if="routeResult.trafficLights">
              <i class="fas fa-traffic-light"></i>
              <div class="stat-info">
                <h3>红绿灯</h3>
                <p>{{ routeResult.trafficLights }}个</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 起终点信息 -->
        <div class="route-points" v-if="routeResult.origin && routeResult.destination">
          <div class="point-info">
            <h3><i class="fas fa-play"></i> 起点</h3>
            <p><strong>地址：</strong>{{ routeResult.origin.address }}</p>
            <p><strong>坐标：</strong>{{ routeResult.origin.longitude }}, {{ routeResult.origin.latitude }}</p>
          </div>
          
          <div class="point-info">
            <h3><i class="fas fa-flag-checkered"></i> 终点</h3>
            <p><strong>地址：</strong>{{ routeResult.destination.address }}</p>
            <p><strong>坐标：</strong>{{ routeResult.destination.longitude }}, {{ routeResult.destination.latitude }}</p>
          </div>
        </div>

        <!-- 详细路线步骤 -->
        <div class="route-steps" v-if="routeResult.steps && routeResult.steps.length > 0">
          <h3><i class="fas fa-list-ol"></i> 详细路线</h3>
          <div class="steps-list">
            <div 
              class="step-item" 
              v-for="(step, index) in routeResult.steps" 
              :key="index"
            >
              <div class="step-number">{{ index + 1 }}</div>
              <div class="step-content">
                <h4>{{ step.instruction }}</h4>
                <div class="step-details">
                  <span class="step-distance">
                    <i class="fas fa-route"></i>
                    {{ formatDistance(step.distance) }}
                  </span>
                  <span class="step-duration">
                    <i class="fas fa-clock"></i>
                    {{ formatDuration(step.duration) }}
                  </span>
                  <span class="step-road" v-if="step.roadName">
                    <i class="fas fa-road"></i>
                    {{ step.roadName }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 限行信息 -->
        <div class="restriction-info" v-if="routeResult.restrictionInfo">
          <h3><i class="fas fa-exclamation-triangle"></i> 限行信息</h3>
          <div class="restriction-content">
            <p>{{ routeResult.restrictionInfo }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 错误信息展示 -->
    <div class="error-section" v-if="errorMessage">
      <div class="error-container">
        <div class="error-content">
          <i class="fas fa-exclamation-circle"></i>
          <h3>规划失败</h3>
          <p>{{ errorMessage }}</p>
          <button class="btn btn-primary" @click="clearError">
            <i class="fas fa-redo"></i>
            重新规划
          </button>
        </div>
      </div>
    </div>

    <!-- 快速规划工具 -->
    <div class="quick-planning-section">
      <div class="quick-container">
        <h2><i class="fas fa-bolt"></i> 快速规划</h2>
        <p>简化版路线规划，快速获取基本路线信息</p>
        
        <div class="quick-form">
          <div class="quick-inputs">
            <input 
              type="text" 
              v-model="quickForm.origin" 
              placeholder="起点"
              class="quick-input"
            >
            <input 
              type="text" 
              v-model="quickForm.destination" 
              placeholder="终点"
              class="quick-input"
            >
            <select v-model="quickForm.transportMode" class="quick-select">
              <option value="driving">驾车</option>
              <option value="walking">步行</option>
              <option value="transit">公交</option>
              <option value="riding">骑行</option>
            </select>
            <button 
              class="btn btn-quick" 
              @click="quickPlanRoute" 
              :disabled="isQuickLoading"
            >
              <i class="fas fa-bolt" v-if="!isQuickLoading"></i>
              <i class="fas fa-spinner fa-spin" v-else></i>
              {{ isQuickLoading ? '规划中...' : '快速规划' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import ApiService from '../services/api.js'

export default {
  name: 'RoutePlanning',
  setup() {
    // 响应式数据
    const isLoading = ref(false)
    const isQuickLoading = ref(false)
    const routeResult = ref(null)
    const errorMessage = ref('')
    
    // 路线规划表单
    const routeForm = reactive({
      origin: '',
      destination: '',
      waypoints: '',
      transportMode: 'driving',
      city: '石家庄',
      strategy: '0',
      returnDetailedInfo: true,
      avoidRestriction: false,
      plateNumber: '',
      coordinateType: 'gcj02'
    })
    
    // 快速规划表单
    const quickForm = reactive({
      origin: '',
      destination: '',
      transportMode: 'driving'
    })
    
    // 路线规划方法
    const planRoute = async () => {
      if (!routeForm.origin || !routeForm.destination) {
        errorMessage.value = '请填写起点和终点'
        return
      }
      
      isLoading.value = true
      errorMessage.value = ''
      routeResult.value = null
      
      try {
        // 构建请求数据
        const requestData = {
          origin: routeForm.origin,
          destination: routeForm.destination,
          transportMode: routeForm.transportMode,
          city: routeForm.city,
          strategy: routeForm.strategy,
          returnDetailedInfo: routeForm.returnDetailedInfo,
          coordinateType: routeForm.coordinateType,
          avoidRestriction: routeForm.avoidRestriction,
          timestamp: Date.now(),
          userId: 'web_user_' + Date.now()
        }
        
        // 添加途经点
        if (routeForm.waypoints) {
          requestData.waypoints = routeForm.waypoints.split(';').map(point => point.trim()).filter(point => point)
        }
        
        // 添加车牌号
        if (routeForm.avoidRestriction && routeForm.plateNumber) {
          requestData.plateNumber = routeForm.plateNumber
        }
        
        // 使用API服务发送请求
        const response = await ApiService.routePlanning.planRoute(requestData)
        
        if (response.success) {
          routeResult.value = response.route
        } else {
          errorMessage.value = response.message || '路线规划失败'
        }
        
      } catch (error) {
        console.error('路线规划错误:', error)
        if (error.response) {
          errorMessage.value = error.response.data.message || '服务器错误'
        } else if (error.request) {
          errorMessage.value = '网络错误，请检查Java后端服务是否启动（端口8080）'
        } else {
          errorMessage.value = '请求配置错误'
        }
      } finally {
        isLoading.value = false
      }
    }
    
    // 快速规划方法
    const quickPlanRoute = async () => {
      if (!quickForm.origin || !quickForm.destination) {
        errorMessage.value = '请填写起点和终点'
        return
      }
      
      isQuickLoading.value = true
      errorMessage.value = ''
      routeResult.value = null
      
      try {
        // 使用API服务发送快速规划请求
        const response = await ApiService.routePlanning.quickPlan(
          quickForm.origin,
          quickForm.destination,
          quickForm.transportMode,
          '石家庄'
        )
        
        if (response.success) {
          routeResult.value = response.route
        } else {
          errorMessage.value = response.message || '快速规划失败'
        }
        
      } catch (error) {
        console.error('快速规划错误:', error)
        if (error.response) {
          errorMessage.value = error.response.data.message || '服务器错误'
        } else if (error.request) {
          errorMessage.value = '网络错误，请检查Java后端服务是否启动（端口8080）'
        } else {
          errorMessage.value = '请求配置错误'
        }
      } finally {
        isQuickLoading.value = false
      }
    }
    
    // 清空表单
    const clearForm = () => {
      Object.assign(routeForm, {
        origin: '',
        destination: '',
        waypoints: '',
        transportMode: 'driving',
        city: '石家庄',
        strategy: '0',
        returnDetailedInfo: true,
        avoidRestriction: false,
        plateNumber: '',
        coordinateType: 'gcj02'
      })
      routeResult.value = null
      errorMessage.value = ''
    }
    
    // 清除错误
    const clearError = () => {
      errorMessage.value = ''
    }
    
    // 格式化距离
    const formatDistance = (distance) => {
      if (!distance) return '0米'
      if (distance >= 1000) {
        return (distance / 1000).toFixed(1) + '公里'
      }
      return distance + '米'
    }
    
    // 格式化时间
    const formatDuration = (duration) => {
      if (!duration) return '0分钟'
      const hours = Math.floor(duration / 3600)
      const minutes = Math.floor((duration % 3600) / 60)
      
      if (hours > 0) {
        return `${hours}小时${minutes}分钟`
      }
      return `${minutes}分钟`
    }
    
    // 组件挂载时检查后端服务状态
    onMounted(async () => {
      try {
        await ApiService.routePlanning.healthCheck()
        console.log('Java后端服务连接正常')
      } catch (error) {
        console.warn('Java后端服务连接失败，请确保服务已启动在端口8080')
      }
    })
    
    return {
      isLoading,
      isQuickLoading,
      routeResult,
      errorMessage,
      routeForm,
      quickForm,
      planRoute,
      quickPlanRoute,
      clearForm,
      clearError,
      formatDistance,
      formatDuration
    }
  }
}
</script>

<style scoped>
/* 页面容器 */
.route-planning-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.page-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-weight: 700;
}

.page-header p {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
}

/* 表单区域 */
.planning-form-section {
  margin-bottom: 40px;
}

.form-container {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
  border: 1px solid #e1e8ed;
}

.form-container h2 {
  color: #2c3e50;
  margin-bottom: 25px;
  font-size: 1.5rem;
  font-weight: 600;
}

/* 表单样式 */
.route-form {
  display: grid;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  color: #34495e;
  margin-bottom: 8px;
  font-size: 0.95rem;
}

.form-group label i {
  margin-right: 8px;
  color: #3498db;
  width: 16px;
}

.form-group input,
.form-group select {
  padding: 12px 15px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #fafbfc;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3498db;
  background: white;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

/* 高级选项 */
.advanced-options {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #e9ecef;
}

.advanced-options h3 {
  color: #495057;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 15px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-weight: 500;
  color: #495057;
}

.checkbox-label input[type="checkbox"] {
  margin-right: 10px;
  transform: scale(1.2);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group.half {
  margin: 0;
}

/* 按钮样式 */
.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 10px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  flex: 1;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #2980b9, #1f5f8b);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
  transform: translateY(-2px);
}

/* 结果展示区域 */
.route-result-section {
  margin-bottom: 40px;
}

.result-container {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.1);
  border: 1px solid #e1e8ed;
}

.result-container h2 {
  color: #27ae60;
  margin-bottom: 25px;
  font-size: 1.5rem;
  font-weight: 600;
}

/* 路线概览 */
.route-overview {
  margin-bottom: 30px;
}

.overview-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 15px;
  border: 1px solid #dee2e6;
}

.stat-card i {
  font-size: 2rem;
  color: #3498db;
}

.stat-info h3 {
  margin: 0 0 5px 0;
  color: #495057;
  font-size: 0.9rem;
  font-weight: 600;
}

.stat-info p {
  margin: 0;
  color: #2c3e50;
  font-size: 1.2rem;
  font-weight: 700;
}

/* 起终点信息 */
.route-points {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.point-info {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #e9ecef;
}

.point-info h3 {
  color: #495057;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.point-info p {
  margin: 5px 0;
  color: #6c757d;
  font-size: 0.9rem;
}

.point-info strong {
  color: #495057;
}

/* 路线步骤 */
.route-steps {
  margin-bottom: 30px;
}

.route-steps h3 {
  color: #495057;
  margin-bottom: 20px;
  font-size: 1.2rem;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.step-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 10px;
  border: 1px solid #e9ecef;
}

.step-number {
  background: #3498db;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-content h4 {
  margin: 0 0 10px 0;
  color: #2c3e50;
  font-size: 1rem;
  font-weight: 600;
}

.step-details {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.step-details span {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #6c757d;
  font-size: 0.85rem;
}

.step-details i {
  color: #3498db;
}

/* 限行信息 */
.restriction-info {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 10px;
  padding: 20px;
}

.restriction-info h3 {
  color: #856404;
  margin-bottom: 10px;
  font-size: 1.1rem;
}

.restriction-content p {
  color: #856404;
  margin: 0;
  font-weight: 500;
}

/* 错误信息 */
.error-section {
  margin-bottom: 40px;
}

.error-container {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 15px;
  padding: 30px;
  text-align: center;
}

.error-content {
  color: #721c24;
}

.error-content i {
  font-size: 3rem;
  margin-bottom: 15px;
  color: #dc3545;
}

.error-content h3 {
  margin-bottom: 10px;
  font-size: 1.3rem;
}

.error-content p {
  margin-bottom: 20px;
  font-size: 1rem;
}

/* 快速规划 */
.quick-planning-section {
  margin-bottom: 40px;
}

.quick-container {
  background: linear-gradient(135deg, #74b9ff, #0984e3);
  color: white;
  padding: 30px;
  border-radius: 15px;
  text-align: center;
}

.quick-container h2 {
  margin-bottom: 10px;
  font-size: 1.5rem;
}

.quick-container p {
  margin-bottom: 25px;
  opacity: 0.9;
}

.quick-form {
  max-width: 800px;
  margin: 0 auto;
}

.quick-inputs {
  display: grid;
  grid-template-columns: 1fr 1fr auto auto;
  gap: 15px;
  align-items: center;
}

.quick-input,
.quick-select {
  padding: 12px 15px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  color: #2c3e50;
}

.quick-input:focus,
.quick-select:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(255,255,255,0.3);
}

.btn-quick {
  background: #00b894;
  color: white;
  white-space: nowrap;
}

.btn-quick:hover:not(:disabled) {
  background: #00a085;
  transform: translateY(-2px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .route-planning-container {
    padding: 15px;
  }
  
  .page-header {
    padding: 30px 15px;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .form-container,
  .result-container,
  .quick-container {
    padding: 20px;
  }
  
  .overview-stats {
    grid-template-columns: 1fr;
  }
  
  .route-points {
    grid-template-columns: 1fr;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .quick-inputs {
    grid-template-columns: 1fr;
  }
  
  .step-details {
    flex-direction: column;
    gap: 10px;
  }
}

@media (max-width: 480px) {
  .page-header h1 {
    font-size: 1.5rem;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
  
  .step-item {
    flex-direction: column;
    gap: 10px;
  }
  
  .step-number {
    align-self: flex-start;
  }
}
</style>