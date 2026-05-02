# 灵境行者 - Vue3前端应用

灵境行者是一个基于Vue3的骑行应用前端，提供路线规划、装备推荐、VR体验、数据可视化等功能。

## 🚀 功能特性

### 核心功能
- **用户认证**: 用户注册、登录、个人资料管理
- **路线规划**: 基于高德地图的智能骑行路线规划
- **装备推荐**: 集成Python后端的装备搜索和推荐
- **数据可视化**: 多种图表展示装备市场分析
  - 价格历史趋势图：展示单类产品多平台历史价格变化
  - 品牌市场份额图：显示不同品牌在各类别中的占有率
  - 价格分布统计图：分析不同价格区间的产品分布
  - 品牌综合评分雷达图：多维度对比品牌评分
- **VR体验**: 沉浸式骑行路线预览
- **反馈系统**: 用户反馈收集和管理
- **帮助中心**: 完整的使用指南
- **安全指南**: 骑行安全知识
- **维护保养指南**: 自行车维护保养知识
- **骑行活动日历**: 骑行活动信息展示
- **非遗骑行地图**: 文化骑行路线展示

### 页面路由
- `/` - 首页（地图展示和路线规划）
- `/login` - 用户登录
- `/register` - 用户注册
- `/route-planning` - 详细路线规划（需要登录）
- `/feedback` - 反馈提交（需要登录）
- `/vr` - VR体验（需要登录）
- `/help` - 帮助中心
- `/safety-guide` - 安全指南
- `/maintenance-guide` - 维护保养指南
- `/event-calendar` - 骑行活动日历
- `/equipment` - 装备展示
- `/intangible-heritage-map` - 非遗骑行地图

## 🛠️ 技术栈

- **框架**: Vue 3.5.13 + Vite 6.2.0
- **路由**: Vue Router 4.5.0
- **HTTP客户端**: Axios 1.9.0
- **地图服务**: 高德地图 JavaScript API
- **图表库**: Chart.js 4.4.9 + Vue-ChartJS 5.3.2
- **图标库**: FontAwesome 6.7.2
- **构建工具**: Vite
- **包管理**: npm

## 📋 环境要求

- Node.js 16+
- npm 8+
- 现代浏览器（支持ES6+）

## 🔧 安装和运行

### 1. 安装依赖
```bash
npm install
```

### 2. 开发环境运行
```bash
npm run dev
```
应用将在 `http://localhost:5173` 启动

### 3. 生产环境构建
```bash
npm run build
```

### 4. 预览生产构建
```bash
npm run preview
```

## 🔌 后端服务配置

### Java后端（主要API服务）
- **地址**: `http://localhost:8080`
- **功能**: 路线规划、用户认证、数据库操作
- **文档**: 参见 `API_ENDPOINTS.md`

### Python后端（爬虫服务）
- **地址**: `http://localhost:5000/api`
- **功能**: 装备爬取、搜索、推荐、数据分析
- **文档**: 参见 `../python-backend/README.md`

## 🗺️ 高德地图配置

项目使用高德地图API，配置信息：
- **Web JS API Key**: `cc888f3fbd2b5c82cb3b842d8277c241`
- **Web服务API Key**: `4b19117847fdee44a92d547edb7ab8c1`
- **安全密钥**: `045a4882fc3282b9bf01d689b11a06d7`

## 📁 项目结构

```
src/
├── components/          # 可复用组件
│   ├── Navbar.vue
│   ├── Footer.vue
│   ├── PriceHistoryChart.vue
│   ├── BrandMarketShareChart.vue
│   ├── PriceDistributionChart.vue
│   └── BrandRadarChart.vue
├── views/              # 页面组件
│   ├── Home.vue        # 首页
│   ├── Login.vue       # 登录页
│   ├── Register.vue    # 注册页
│   ├── RoutePlanning.vue # 路线规划
│   ├── Feedback.vue    # 反馈页面
│   ├── VR.vue          # VR体验
│   ├── Help.vue        # 帮助页面
│   ├── Equipment.vue   # 装备展示
│   ├── SafetyGuide.vue # 安全指南
│   ├── MaintenanceGuide.vue # 维护保养
│   ├── EventCalendar.vue # 活动日历
│   └── IntangibleHeritageMap.vue # 非遗地图
├── router/             # 路由配置
│   └── index.js
├── services/           # API服务
│   └── api.js
├── utils/              # 工具函数
│   ├── auth.js
│   └── database.js
├── config/             # 配置文件
│   ├── api.js
│   └── database.js
└── assets/             # 静态资源
    └── styles/
```

## 🔐 认证和权限

- 使用JWT token进行用户认证
- 部分页面需要登录访问（通过路由守卫控制）
- 支持自动登录状态检查
- 需要认证的页面: `/feedback`, `/vr`, `/route-planning`

## 📡 API集成

### Java后端API
- 路线规划: `/route/plan`, `/route/quick-plan`
- 用户认证: `/auth/*`
- 用户管理: `/user/*`
- 反馈管理: `/feedback`
- 地理编码: `/route/geocode`, `/route/reverse-geocode`

### Python后端API
- 装备搜索: `/api/equipment/search`
- 装备详情: `/api/equipment/<id>`
- 爬虫控制: `/api/equipment/crawl`
- 分类管理: `/api/equipment/categories`
- 数据分析: `/api/analysis/*`
- 图表数据: `/api/analysis/price-history`, `/api/analysis/brand-market-share`, `/api/analysis/price-distribution`

## 🚀 部署说明

### 开发环境
1. 确保Java后端在8080端口运行
2. 确保Python后端在5000端口运行
3. 运行 `npm run dev` 启动前端

### 生产环境
1. 修改 `src/config/api.js` 中的生产环境API地址
2. 运行 `npm run build` 构建
3. 将 `dist` 目录部署到Web服务器

## 📝 开发指南

### 添加新页面
1. 在 `src/views/` 创建Vue组件
2. 在 `src/router/index.js` 添加路由配置
3. 如需认证，添加 `meta: { requiresAuth: true }`

### API调用
使用 `src/services/api.js` 中的ApiService类：
```javascript
import { ApiService } from '@/services/api.js'

// 调用API
const result = await ApiService.routes.getAll()
```

### 地图功能
参考 `src/views/Home.vue` 和 `src/views/RoutePlanning.vue` 中的地图集成示例。

## 🐛 常见问题

1. **地图不显示**: 检查高德地图API Key是否正确
2. **API调用失败**: 确认后端服务是否正常运行
3. **路由跳转异常**: 检查路由配置和认证状态
4. **跨域问题**: 确保后端CORS配置正确

## 📄 相关文档

- [API接口文档](./API_ENDPOINTS.md)
- [数据库设置指南](./DATABASE_SETUP.md)
- [Java后端文档](../java-backend/README.md)
- [Python后端文档](../python-backend/README.md)

---

*最后更新：2025年5月*
