<template>
  <div class="route-planning-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1><i class="fas fa-route"></i> 智能路线规划</h1>
      <p>基于高德地图API的专业骑行路线规划服务，探索最美骑行路线</p>
    </div>

    <!-- 地图和控制面板区域 -->
    <section class="map-section">
      <!-- 优化后的地图容器 - 支持高德地图API -->
      <div id="container" class="map-container">
        <!-- 地图将通过高德地图API加载 -->
        <!-- 需接入高德地图API -->
      </div>
      
      <!-- 地图控制面板 - 支持起点终点选择 -->
      <div class="map-controls">
        <h3><i class="fas fa-map-marked-alt"></i> 路线规划</h3>
        
        <div class="control-group">
          <label for="startPoint"><i class="fas fa-play"></i> 起点</label>
          <input type="text" id="startPoint" placeholder="输入或点击地图选择起点">
        </div>
        
        <div class="control-group">
          <label for="endPoint"><i class="fas fa-flag-checkered"></i> 终点</label>
          <input type="text" id="endPoint" placeholder="输入或点击地图选择终点">
        </div>
        
        <button class="btn btn-full" id="calculateRoute">
          <i class="fas fa-route"></i> 规划路线
        </button>
      </div>
    </section>
    
    <!-- 路线信息展示区域 -->
    <section class="route-info-section">
      <div class="info-main">
        <div class="route-header">
          <span class="difficulty easy">智能规划</span>
          <h1>个性化骑行路线</h1>
          
          <div class="route-stats">
            <div class="stat-item">
              <i class="fas fa-route"></i>
              <h4>距离</h4>
              <p id="route-distance">-- 公里</p>
            </div>
            <div class="stat-item">
              <i class="far fa-clock"></i>
              <h4>时间</h4>
              <p id="route-duration">-- 分钟</p>
            </div>
            <div class="stat-item">
              <i class="fas fa-mountain"></i>
              <h4>难度</h4>
              <p id="route-difficulty">智能评估</p>
            </div>
            <div class="stat-item">
              <i class="fas fa-road"></i>
              <h4>路面</h4>
              <p id="route-surface">混合路面</p>
            </div>
          </div>
        </div>
        
        <div class="route-description">
          <p>智能路线规划系统将根据您的起点和终点，为您推荐最适合的骑行路线。系统会综合考虑道路状况、安全性、景观质量等多个因素，为您提供个性化的骑行体验。</p>
        </div>
        
        <!-- 折叠面板 - 路线概览 -->
        <div class="collapsible-panel">
          <div class="panel-header" onclick="togglePanel(this)">
            <h3><i class="fas fa-info-circle"></i> 路线概览</h3>
            <span>+</span>
          </div>
          <div class="panel-content">
            <p>系统将为您生成详细的路线信息，包括具体的行驶路径、途经地点、注意事项等。</p>
            
            <ul id="route-overview-list">
              <li><strong>起点:</strong> <span id="start-address">待规划</span></li>
              <li><strong>终点:</strong> <span id="end-address">待规划</span></li>
              <li><strong>路线类型:</strong> <span id="route-type">骑行路线</span></li>
              <li><strong>推荐时段:</strong> <span id="recommended-time">全天候</span></li>
            </ul>
          </div>
        </div>
        
        <!-- 折叠面板 - 路线详情 -->
        <div class="collapsible-panel">
          <div class="panel-header" onclick="togglePanel(this)">
            <h3><i class="fas fa-list-ol"></i> 路线详情</h3>
            <span>+</span>
          </div>
          <div class="panel-content">
            <div id="route-steps">
              <p>规划路线后，这里将显示详细的行驶指引和路线步骤。</p>
            </div>
          </div>
        </div>
        
        <!-- 折叠面板 - 海拔剖面 -->
        <div class="collapsible-panel">
          <div class="panel-header" onclick="togglePanel(this)">
            <h3><i class="fas fa-chart-area"></i> 海拔剖面</h3>
            <span>+</span>
          </div>
          <div class="panel-content">
            <div class="elevation-profile">
              <p>海拔剖面图将在路线规划完成后显示，帮助您了解路线的起伏情况。</p>
            </div>
          </div>
        </div>
        
        <!-- 折叠面板 - 骑行小贴士 -->
        <div class="collapsible-panel">
          <div class="panel-header" onclick="togglePanel(this)">
            <h3><i class="fas fa-lightbulb"></i> 骑行小贴士</h3>
            <span>+</span>
          </div>
          <div class="panel-content">
            <p>为了让您的骑行更加愉快安全，我们提供以下建议：</p>
            <ul>
              <li><strong>出行准备:</strong> 检查车辆状况，携带必要的维修工具和急救包</li>
              <li><strong>安全装备:</strong> 佩戴头盔，穿着反光衣物，确保夜间骑行安全</li>
              <li><strong>天气关注:</strong> 关注天气变化，避免在恶劣天气条件下骑行</li>
              <li><strong>路线熟悉:</strong> 提前了解路线情况，标记重要地标和休息点</li>
              <li><strong>体力分配:</strong> 合理安排骑行节奏，适时休息补充水分</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="info-sidebar">
        <!-- 快速规划工具 -->
        <div class="sidebar-section">
          <h3><i class="fas fa-bolt"></i> 快速规划</h3>
          <div class="quick-planning">
            <input type="text" id="quick-start" placeholder="快速起点" class="quick-input">
            <input type="text" id="quick-end" placeholder="快速终点" class="quick-input">
            <button class="btn btn-quick" onclick="quickPlan()">
              <i class="fas fa-bolt"></i> 快速规划
            </button>
          </div>
        </div>
        
        <!-- 常用地点 -->
        <div class="sidebar-section">
          <h3><i class="fas fa-star"></i> 常用地点</h3>
          <div class="common-places">
            <div class="place-item" onclick="setLocation('石家庄火车站', 'start')">
              <i class="fas fa-train"></i>
              <span>石家庄火车站</span>
            </div>
            <div class="place-item" onclick="setLocation('石家庄机场', 'start')">
              <i class="fas fa-plane"></i>
              <span>石家庄机场</span>
            </div>
            <div class="place-item" onclick="setLocation('河北经贸大学', 'start')">
              <i class="fas fa-university"></i>
              <span>河北经贸大学</span>
            </div>
            <div class="place-item" onclick="setLocation('石家庄市政府', 'start')">
              <i class="fas fa-building"></i>
              <span>石家庄市政府</span>
            </div>
          </div>
        </div>
        
        <!-- 天气信息 -->
        <div class="sidebar-section">
          <h3><i class="fas fa-cloud-sun"></i> 今日天气</h3>
          <div class="weather-info">
            <p>晴朗，22°C-28°C，东北风1-2级</p>
            <p>空气质量: 优 (AQI: 45)</p>
            <p>骑行指数: <strong style="color: #2ecc71;">非常适宜</strong></p>
          </div>
        </div>
        
        <!-- 推荐路线 -->
        <div class="sidebar-section">
          <h3><i class="fas fa-thumbs-up"></i> 推荐路线</h3>
          <div class="recommended-routes">
            <div class="mini-route-card">
              <img src="/source/湖滨休闲道.jpg" alt="湖滨休闲道">
              <div class="mini-route-info">
                <h4>湖滨休闲道</h4>
                <p>12公里 · 初级</p>
              </div>
            </div>
            <div class="mini-route-card">
              <img src="/source/森林山地线.jpg" alt="森林山地线">
              <div class="mini-route-info">
                <h4>森林山地线</h4>
                <p>25公里 · 中级</p>
              </div>
            </div>
            <div class="mini-route-card">
              <img src="/source/海岸风景道.jpg" alt="海岸风景道">
              <div class="mini-route-info">
                <h4>海岸风景道</h4>
                <p>40公里 · 高级</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 用户交互区域 -->
    <section class="user-actions">
      <div class="action-card">
        <h3><i class="fas fa-save"></i> 保存路线</h3>
        <p>将规划好的路线保存到个人收藏</p>
        <button class="btn btn-action" onclick="saveRoute()">
          <i class="fas fa-bookmark"></i> 保存路线
        </button>
      </div>
      
      <div class="action-card">
        <h3><i class="fas fa-share-alt"></i> 分享路线</h3>
        <p>与好友分享这条精心规划的路线</p>
        <div class="share-buttons">
          <a href="#" class="share-btn wechat"><i class="fab fa-weixin"></i></a>
          <a href="#" class="share-btn weibo"><i class="fab fa-weibo"></i></a>
          <a href="#" class="share-btn qq"><i class="fab fa-qq"></i></a>
        </div>
      </div>
      
      <div class="action-card">
        <h3><i class="fas fa-download"></i> 导出路线</h3>
        <p>导出GPX格式文件，导入到骑行设备</p>
        <button class="btn btn-action" onclick="exportRoute()">
          <i class="fas fa-file-export"></i> 导出GPX
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const map = ref(null)
const startPoint = ref('')
const endPoint = ref('')
const routePlanning = ref(null)

// 动态加载高德地图API脚本
const loadAMapScript = () => {
  return new Promise((resolve, reject) => {
    if (window.AMap) {
      resolve(window.AMap)
      return
    }
    
    const script = document.createElement('script')
    script.type = 'text/javascript'
    script.async = true
    script.src = 'https://webapi.amap.com/maps?v=1.4.15&key=cc888f3fbd2b5c82cb3b842d8277c241&plugin=AMap.Riding,AMap.Geocoder,AMap.ToolBar,AMap.Scale&jscode=045a4882fc3282b9bf01d689b11a06d7'
    script.onload = () => {
      if (window.AMap) {
        resolve(window.AMap)
      } else {
        reject(new Error('高德地图API加载失败'))
      }
    }
    script.onerror = () => reject(new Error('高德地图API脚本加载失败'))
    document.head.appendChild(script)
  })
}

// 初始化高德地图
const initAMap = async () => {
  try {
    // 配置高德地图安全密钥（必须在加载API之前设置）
    window._AMapSecurityConfig = {
      securityJSCode: '045a4882fc3282b9bf01d689b11a06d7'
    }
    
    // 动态加载高德地图API
    await loadAMapScript()
    
    // 等待DOM更新
    await nextTick()
    
    // 检查容器是否存在
    const container = document.getElementById('container')
    if (!container) {
      console.error('地图容器不存在')
      return
    }
    
    // 创建地图实例
    map.value = new AMap.Map('container', {
      zoom: 12,
      center: [114.31667, 30.51667], // 石家庄坐标
      resizeEnable: true,
      viewMode: '2D',
      mapStyle: 'amap://styles/normal'
    })
    
    // 监听地图加载完成事件
    map.value.on('complete', () => {
      console.log('地图加载完成')
      // 在地图中心添加一个标记
      const marker = new AMap.Marker({
        position: [114.31667, 30.51667],
        title: '石家庄市中心'
      })
      map.value.add(marker)
    })
    
    // 添加地图控件
    AMap.plugin(['AMap.ToolBar', 'AMap.Scale'], function() {
      // 工具条控件
      map.value.addControl(new AMap.ToolBar({
        position: 'RB'
      }))
      
      // 比例尺控件
      map.value.addControl(new AMap.Scale())
    })
    
    // 初始化骑行路线规划服务
    AMap.plugin('AMap.Riding', function() {
      routePlanning.value = new AMap.Riding({
        map: map.value,
        panel: null,
        policy: AMap.RidingPolicy.LEAST_TIME // 骑行策略参数
      })
    })
    
    console.log('高德地图初始化成功')
  } catch (error) {
    console.error('高德地图初始化失败:', error)
  }
}

// 使用POI搜索API进行地址解析
const geocodeAddress = async (address) => {
  try {
    // 安全密钥
    const securityJsCode = '045a4882fc3282b9bf01d689b11a06d7'
    
    // 首先尝试POI搜索API，这对地标和模糊地址更友好
    const poiUrl = `https://restapi.amap.com/v3/place/text?key=4b19117847fdee44a92d547edb7ab8c1&keywords=${encodeURIComponent(address)}&city=石家庄&offset=1&jscode=${securityJsCode}`
    console.log('尝试POI搜索:', address)
    console.log('POI搜索URL:', poiUrl)
    
    const poiResponse = await fetch(poiUrl)
    const poiData = await poiResponse.json()
    
    console.log('POI搜索响应:', poiData)
    
    // 如果POI搜索成功
    if (poiData.status === '1' && poiData.pois && poiData.pois.length > 0) {
      const poi = poiData.pois[0]
      const location = poi.location.split(',')
      console.log(`POI搜索成功，找到: ${poi.name}，地址: ${poi.address}`)
      return new AMap.LngLat(parseFloat(location[0]), parseFloat(location[1]))
    }
    
    console.log('POI搜索未找到结果，尝试地理编码API')
    
    // 如果POI搜索失败，回退到地理编码API
    const geoUrl = `https://restapi.amap.com/v3/geocode/geo?key=4b19117847fdee44a92d547edb7ab8c1&address=${encodeURIComponent(address)}&jscode=${securityJsCode}`
    console.log('地理编码URL:', geoUrl)
    
    const geoResponse = await fetch(geoUrl)
    const geoData = await geoResponse.json()
    
    console.log('地理编码响应:', geoData)
    
    if (geoData.status === '1' && geoData.geocodes && geoData.geocodes.length > 0) {
      const location = geoData.geocodes[0].location.split(',')
      console.log(`地理编码成功，地址: ${geoData.geocodes[0].formatted_address}`)
      return new AMap.LngLat(parseFloat(location[0]), parseFloat(location[1]))
    }
    
    // 两种方法都失败
    const errorMsg = poiData.info || geoData.info || '未知错误'
    throw new Error(`地址解析失败: ${errorMsg}`)
    
  } catch (error) {
    console.error('地址解析异常:', error)
    if (error.message.includes('地址解析失败:')) {
      throw error
    }
    throw new Error('地址解析请求失败: ' + error.message)
  }
}

// 使用Web服务API进行骑行路线规划
const planBicyclingRoute = async (origin, destination) => {
  try {
    const securityJsCode = '045a4882fc3282b9bf01d689b11a06d7'
    const apiKey = '4b19117847fdee44a92d547edb7ab8c1'
    
    // 使用高德地图Web服务API的骑行路线规划
    const routeUrl = `https://restapi.amap.com/v4/direction/bicycling?key=${apiKey}&origin=${origin}&destination=${destination}&jscode=${securityJsCode}`
    
    console.log('骑行路线规划URL:', routeUrl)
    
    const response = await fetch(routeUrl)
    const data = await response.json()
    
    console.log('骑行路线规划响应:', data)
    
    // 检查API响应格式：{data: {...}, errcode: 0, errmsg: 'OK'}
    if (data.errcode === 0 && data.data && data.data.paths && data.data.paths.length > 0) {
      const path = data.data.paths[0]
      console.log('路线规划成功:', {
        distance: path.distance + '米',
        duration: Math.round(path.duration / 60) + '分钟',
        steps: path.steps.length + '个步骤'
      })
      
      // 在地图上绘制路线
      drawRouteOnMap(path)
      
      // 更新页面信息
      updateRouteInfo(path)
      
      alert(`路线规划成功！\n距离: ${(path.distance / 1000).toFixed(1)}公里\n预计时间: ${Math.round(path.duration / 60)}分钟`)
      return data
    } else {
      throw new Error(data.errmsg || '路线规划失败')
    }
  } catch (error) {
    console.error('骑行路线规划失败:', error)
    throw error
  }
}

// 在地图上绘制路线
const drawRouteOnMap = (path) => {
  if (!map.value) return
  
  try {
    // 清除之前的路线
    map.value.clearMap()
    
    // 解析路径坐标
    const pathCoords = []
    if (path.steps && path.steps.length > 0) {
      path.steps.forEach(step => {
        if (step.polyline) {
          const coords = step.polyline.split(';')
          coords.forEach(coord => {
            const [lng, lat] = coord.split(',')
            if (lng && lat) {
              pathCoords.push([parseFloat(lng), parseFloat(lat)])
            }
          })
        }
      })
    }
    
    if (pathCoords.length > 0) {
      // 创建路线折线
      const polyline = new AMap.Polyline({
        path: pathCoords,
        strokeColor: '#3366FF',
        strokeWeight: 6,
        strokeOpacity: 0.8
      })
      
      map.value.add(polyline)
      
      // 添加起点和终点标记
      const startMarker = new AMap.Marker({
        position: pathCoords[0],
        title: '起点',
        icon: new AMap.Icon({
          size: new AMap.Size(25, 34),
          image: 'https://webapi.amap.com/theme/v1.3/markers/n/start.png'
        })
      })
      
      const endMarker = new AMap.Marker({
        position: pathCoords[pathCoords.length - 1],
        title: '终点',
        icon: new AMap.Icon({
          size: new AMap.Size(25, 34),
          image: 'https://webapi.amap.com/theme/v1.3/markers/n/end.png'
        })
      })
      
      map.value.add([startMarker, endMarker])
      
      // 调整地图视野以显示完整路线
      map.value.setFitView([polyline])
    }
  } catch (error) {
    console.error('绘制路线失败:', error)
  }
}

// 更新路线信息
const updateRouteInfo = (path) => {
  // 更新距离
  const distanceElement = document.getElementById('route-distance')
  if (distanceElement) {
    distanceElement.textContent = `${(path.distance / 1000).toFixed(1)} 公里`
  }
  
  // 更新时间
  const durationElement = document.getElementById('route-duration')
  if (durationElement) {
    durationElement.textContent = `${Math.round(path.duration / 60)} 分钟`
  }
  
  // 更新路线步骤
  const stepsElement = document.getElementById('route-steps')
  if (stepsElement && path.steps) {
    let stepsHtml = '<ol>'
    path.steps.forEach((step, index) => {
      stepsHtml += `<li><strong>${step.instruction || '继续前行'}</strong>`
      if (step.road_name) {
        stepsHtml += ` - ${step.road_name}`
      }
      if (step.distance) {
        stepsHtml += ` (${step.distance}米)`
      }
      stepsHtml += '</li>'
    })
    stepsHtml += '</ol>'
    stepsElement.innerHTML = stepsHtml
  }
}

// 规划路线
const calculateRoute = async () => {
  const startInput = document.getElementById('startPoint')
  const endInput = document.getElementById('endPoint')
  
  if (!startInput.value || !endInput.value) {
    alert('请输入起点和终点')
    return
  }
  
  try {
    console.log('开始解析起点地址:', startInput.value)
    const startLngLat = await geocodeAddress(startInput.value)
    console.log('起点坐标:', startLngLat.toString())
    
    console.log('开始解析终点地址:', endInput.value)
    const endLngLat = await geocodeAddress(endInput.value)
    console.log('终点坐标:', endLngLat.toString())
    
    // 更新地址显示
    const startAddressElement = document.getElementById('start-address')
    const endAddressElement = document.getElementById('end-address')
    if (startAddressElement) startAddressElement.textContent = startInput.value
    if (endAddressElement) endAddressElement.textContent = endInput.value
    
    // 使用Web服务API进行骑行路线规划
    const origin = `${startLngLat.lng},${startLngLat.lat}`
    const destination = `${endLngLat.lng},${endLngLat.lat}`
    
    await planBicyclingRoute(origin, destination)
    
  } catch (error) {
    console.error('路线规划失败:', error)
    alert('路线规划失败: ' + error.message)
  }
}

// 全局函数定义
window.togglePanel = (header) => {
  const panel = header.parentElement
  const content = panel.querySelector('.panel-content')
  const icon = header.querySelector('span')
  
  if (content.style.display === 'none' || !content.style.display) {
    content.style.display = 'block'
    icon.textContent = '-'
    panel.classList.add('active')
  } else {
    content.style.display = 'none'
    icon.textContent = '+'
    panel.classList.remove('active')
  }
}

window.quickPlan = () => {
  const quickStart = document.getElementById('quick-start')
  const quickEnd = document.getElementById('quick-end')
  const startInput = document.getElementById('startPoint')
  const endInput = document.getElementById('endPoint')
  
  if (quickStart.value) startInput.value = quickStart.value
  if (quickEnd.value) endInput.value = quickEnd.value
  
  calculateRoute()
}

window.setLocation = (location, type) => {
  const input = type === 'start' ? document.getElementById('startPoint') : document.getElementById('endPoint')
  if (input) {
    input.value = location
  }
}

window.saveRoute = () => {
  alert('路线保存功能开发中...')
}

window.exportRoute = () => {
  alert('GPX导出功能开发中...')
}

// 组件挂载时初始化地图
onMounted(async () => {
  // 等待DOM渲染完成后再初始化地图
  await nextTick()
  initAMap()
  
  // 绑定按钮事件
  setTimeout(() => {
    const calculateBtn = document.getElementById('calculateRoute')
    if (calculateBtn) {
      calculateBtn.addEventListener('click', calculateRoute)
    }
    
    // 绑定输入框
    const startInput = document.getElementById('startPoint')
    const endInput = document.getElementById('endPoint')
    
    if (startInput) {
      startInput.addEventListener('input', (e) => {
        startPoint.value = e.target.value
      })
    }
    
    if (endInput) {
      endInput.addEventListener('input', (e) => {
        endPoint.value = e.target.value
      })
    }
  }, 100)
})

// 组件卸载时销毁地图
onUnmounted(() => {
  if (map.value) {
    map.value.destroy()
  }
})
</script>

<style scoped>
/* 页面整体布局 */
.route-planning-page {
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
}

/* 地图区域 */
.map-section {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 30px;
  margin: 0 20px 40px;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
}

.map-container {
  height: 500px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  background: #f8f9fa;
}

.map-controls {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.map-controls h3 {
  color: #2C3E50;
  margin-bottom: 25px;
  font-size: 1.3rem;
  font-weight: 600;
}

.control-group {
  margin-bottom: 20px;
}

.control-group label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
}

.control-group input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.control-group input:focus {
  outline: none;
  border-color: #FF9800;
  box-shadow: 0 0 0 3px rgba(255, 152, 0, 0.1);
}

/* 路线信息区域 */
.route-info-section {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 40px;
  margin: 0 20px;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
}

.info-main {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.route-header h1 {
  font-size: 2.2rem;
  color: #2C3E50;
  margin: 15px 0 30px;
  font-weight: 700;
}

.route-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin: 30px 0;
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

.route-description {
  color: #666;
  line-height: 1.7;
  margin-bottom: 30px;
  font-size: 1rem;
}

/* 折叠面板 */
.collapsible-panel {
  margin-bottom: 20px;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  overflow: hidden;
}

.panel-header {
  background: #f8f9fa;
  padding: 15px 20px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.panel-header:hover {
  background: #e9ecef;
}

.panel-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #2C3E50;
  font-weight: 600;
}

.panel-header span {
  font-size: 1.2rem;
  font-weight: bold;
  color: #FF9800;
}

.panel-content {
  padding: 20px;
  display: none;
  background: white;
}

.collapsible-panel.active .panel-content {
  display: block;
}

.panel-content ul {
  margin: 15px 0;
  padding-left: 20px;
}

.panel-content li {
  margin-bottom: 8px;
  line-height: 1.6;
}

/* 侧边栏 */
.info-sidebar {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.sidebar-section {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.sidebar-section h3 {
  color: #2C3E50;
  margin-bottom: 20px;
  font-size: 1.2rem;
  font-weight: 600;
}

/* 快速规划 */
.quick-planning {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.quick-input {
  padding: 10px 12px;
  border: 2px solid #e1e5e9;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.quick-input:focus {
  outline: none;
  border-color: #FF9800;
}

.btn-quick {
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-quick:hover {
  background: linear-gradient(135deg, #FFB74D, #FF9800);
  transform: translateY(-1px);
}

/* 常用地点 */
.common-places {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.place-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.place-item:hover {
  background: #e9ecef;
  transform: translateX(5px);
}

.place-item i {
  color: #FF9800;
  font-size: 1.1rem;
}

.place-item span {
  font-size: 0.9rem;
  color: #2C3E50;
}

/* 天气信息 */
.weather-info p {
  margin: 8px 0;
  font-size: 0.9rem;
  color: #666;
}

/* 推荐路线 */
.recommended-routes {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.mini-route-card {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.mini-route-card:hover {
  background: #e9ecef;
  transform: translateY(-2px);
}

.mini-route-card img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 6px;
}

.mini-route-info h4 {
  margin: 0 0 5px;
  font-size: 0.95rem;
  color: #2C3E50;
}

.mini-route-info p {
  margin: 0;
  font-size: 0.8rem;
  color: #666;
}

/* 用户交互区域 */
.user-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin: 40px 20px;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
}

.action-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: all 0.3s ease;
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.action-card h3 {
  color: #2C3E50;
  margin-bottom: 15px;
  font-size: 1.3rem;
  font-weight: 600;
}

.action-card p {
  color: #666;
  margin-bottom: 25px;
  line-height: 1.6;
}

.btn-action {
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-action:hover {
  background: linear-gradient(135deg, #FFB74D, #FF9800);
  transform: translateY(-2px);
}

/* 分享按钮 */
.share-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.share-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  color: white;
  text-decoration: none;
  transition: all 0.3s ease;
}

.share-btn.wechat {
  background: #1AAD19;
}

.share-btn.weibo {
  background: #E6162D;
}

.share-btn.qq {
  background: #12B7F5;
}

.share-btn:hover {
  transform: translateY(-3px) scale(1.1);
}

/* 通用按钮样式 */
.btn {
  display: inline-block;
  padding: 14px 28px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  text-align: center;
}

.btn-full {
  width: 100%;
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
}

.btn-full:hover {
  background: linear-gradient(135deg, #FFB74D, #FF9800);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 152, 0, 0.4);
}

/* 难度标签 */
.difficulty {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 25px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 15px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.difficulty.easy {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .map-section {
    grid-template-columns: 1fr;
  }
  
  .route-info-section {
    grid-template-columns: 1fr;
  }
  
  .route-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 40px 15px;
  }
  
  .map-section,
  .route-info-section,
  .user-actions {
    margin: 0 15px 30px;
  }
  
  .info-main {
    padding: 25px;
  }
  
  .route-stats {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .user-actions {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .page-header {
    padding: 30px 10px;
  }
  
  .map-container {
    height: 350px;
  }
  
  .map-controls,
  .info-main,
  .sidebar-section,
  .action-card {
    padding: 20px;
  }
}
</style>