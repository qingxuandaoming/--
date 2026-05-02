# API 端点说明文档

> **更新日期**: 2025年5月

## Java 后端 API (http://localhost:8080)

### 健康检查
- **GET** `/health` - 检查服务状态
- **GET** `/route/health` - 检查路线规划服务状态

### 路线规划服务
- **POST** `/route/plan` - 完整路线规划
  - 请求体示例:
  ```json
  {
    "origin": "石家庄市长安区",
    "destination": "石家庄市裕华区",
    "transportMode": "riding",
    "city": "石家庄",
    "strategy": 0,
    "showSteps": true,
    "waypoints": ["石家庄市桥西区"]
  }
  ```

- **GET** `/route/quick-plan` - 快速路线规划
  - 查询参数: `origin`, `destination`, `transportMode`, `city`
  - 示例: `/route/quick-plan?origin=起点&destination=终点&transportMode=riding`

### 地理编码服务
- **GET** `/route/geocode` - 地址转坐标
  - 查询参数: `address`, `city`
- **GET** `/route/reverse-geocode` - 坐标转地址
  - 查询参数: `longitude`, `latitude`

### 配置信息
- **GET** `/route/transport-modes` - 获取支持的交通方式
- **GET** `/route/strategies` - 获取路线策略选项
- **GET** `/docs` - 获取API文档说明

### 数据库测试
- **GET** `/test` - 基本服务测试
- **GET** `/tables` - 获取数据库表列表
- **GET** `/cycling-routes` - 获取骑行路线列表（模拟数据）
  - 查询参数: `limit` (可选) - 限制返回数量，默认10，最大100

### 用户认证
- **POST** `/auth/login` - 用户登录
  - 请求体: `{ "usernameOrEmail": "xxx", "password": "xxx" }`
- **POST** `/auth/register` - 用户注册
  - 请求体: `{ "username": "xxx", "email": "xxx", "password": "xxx", "confirmPassword": "xxx", "firstName": "xxx", "lastName": "xxx" }`
- **POST** `/auth/refresh` - 刷新Token
  - 请求体: `{ "refreshToken": "xxx" }`
- **POST** `/auth/logout` - 用户登出
- **GET** `/auth/check-username` - 检查用户名是否可用
  - 查询参数: `username`
- **GET** `/auth/check-email` - 检查邮箱是否可用
  - 查询参数: `email`

### 用户管理
- **GET** `/user/profile` - 获取当前用户信息（需要JWT认证）
- **PUT** `/user/profile` - 更新用户信息（需要JWT认证）
  - 请求体: `{ "fullName": "xxx", "phone": "xxx", "avatarUrl": "xxx" }`
- **GET** `/user/records` - 获取用户记录（需要JWT认证）

### 反馈管理
- **POST** `/feedback` - 创建新反馈
- **GET** `/feedback` - 获取反馈列表
- **GET** `/feedback/{id}` - 获取特定反馈
- **PUT** `/feedback/{id}` - 更新反馈
- **DELETE** `/feedback/{id}` - 删除反馈

## Python 后端 API (http://localhost:5000/api)

### 健康检查
- **GET** `/api/health` - 检查Python后端服务状态

### 装备分类管理
- **GET** `/api/equipment/categories` - 获取所有装备分类

### 装备搜索和管理
- **GET** `/api/equipment/search` - 搜索装备
  - 查询参数:
    - `keyword` - 关键词搜索
    - `category_id` - 分类ID
    - `min_price` - 最低价格
    - `max_price` - 最高价格
    - `platform` - 平台筛选
    - `sort_by` - 排序字段（默认rating）
    - `page` - 页码
    - `per_page` - 每页数量

- **GET** `/api/equipment` - 获取装备列表
  - 查询参数: `category_id`, `sort_by`, `page`, `per_page`
- **GET** `/api/equipment/<id>` - 获取装备详情
- **GET** `/api/equipment/<id>/prices` - 获取装备价格历史
  - 查询参数: `days` (默认30)
- **GET** `/api/equipment/<id>/recommendations` - 获取装备推荐

### 爬虫服务
- **POST** `/api/equipment/crawl` - 手动触发爬虫
  - 请求体示例:
  ```json
  {
    "platform": "taobao",
    "category": "helmet"
  }
  ```
- **GET** `/api/equipment/crawl/status/<task_id>` - 获取爬虫任务状态

### 高级爬虫
- **POST** `/api/advanced-crawler/start` - 启动高级爬虫任务
  - 请求体: `{ "platforms": ["taobao","jd"], "categories": ["bike","helmet"], "keywords": [...], "max_items_per_keyword": 50 }`
- **GET** `/api/advanced-crawler/status/<task_id>` - 获取高级爬虫任务状态
- **GET** `/api/advanced-crawler/tasks` - 获取所有高级爬虫任务

### 数据分析
- **GET** `/api/analysis/trends` - 获取装备价格趋势分析
  - 查询参数: `days`
- **GET** `/api/analysis/competition` - 获取市场竞争分析
  - 查询参数: `category`
- **GET** `/api/analysis/price-alerts` - 获取价格预警
  - 查询参数: `threshold`
- **GET** `/api/analysis/recommendations` - 获取装备推荐分析
  - 查询参数: `category`, `platform`, `min_budget`, `max_budget`, `limit`
- **POST** `/api/analysis/clear-cache` - 清理分析缓存

### 图表数据
- **GET** `/api/analysis/price-history/<equipment_id>` - 获取多平台价格历史图表数据
  - 查询参数: `days`
- **GET** `/api/analysis/brand-market-share` - 获取品牌市场份额图表数据
  - 查询参数: `category`
- **GET** `/api/analysis/price-distribution` - 获取价格分布图表数据

### 爬虫配置管理
- **GET** `/api/config/crawler` - 获取爬虫配置
  - 查询参数: `key`
- **PUT** `/api/config/crawler` - 更新爬虫配置
  - 请求体: `{ "key": "xxx", "value": "xxx" }`
- **GET** `/api/config/crawler/summary` - 获取配置摘要
- **GET** `/api/config/crawler/platforms` - 获取启用的平台列表
- **GET** `/api/config/crawler/categories` - 获取启用的分类列表
- **GET** `/api/config/crawler/keywords/<category>` - 获取分类关键词
- **POST** `/api/config/crawler/keywords/<category>` - 添加关键词
- **DELETE** `/api/config/crawler/keywords/<category>` - 移除关键词
- **PUT** `/api/config/crawler/platform/<platform>/status` - 更新平台启用状态
- **PUT** `/api/config/crawler/category/<category>/status` - 更新分类启用状态
- **POST** `/api/config/crawler/reset` - 重置配置为默认值
- **GET** `/api/config/crawler/export` - 导出配置

### 爬虫监控
- **POST** `/api/monitor/start` - 启动监控服务
- **POST** `/api/monitor/stop` - 停止监控服务
- **GET** `/api/monitor/stats/current` - 获取当前爬虫统计
- **GET** `/api/monitor/stats/history` - 获取统计历史
- **GET** `/api/monitor/metrics/current` - 获取当前系统指标
- **GET** `/api/monitor/metrics/history` - 获取系统指标历史
- **GET** `/api/monitor/errors` - 获取错误摘要
- **GET** `/api/monitor/performance` - 获取性能摘要
- **GET** `/api/monitor/database` - 获取数据库统计
- **GET** `/api/monitor/report` - 获取综合监控报告
- **POST** `/api/monitor/clear-history` - 清理监控历史

### 爬虫队列管理
- **POST** `/api/queue/start` - 启动队列服务
- **POST** `/api/queue/stop` - 停止队列服务
- **POST** `/api/queue/tasks` - 创建爬虫任务
- **GET** `/api/queue/tasks` - 获取任务列表
- **GET** `/api/queue/tasks/<task_id>` - 获取单个任务
- **POST** `/api/queue/tasks/<task_id>/cancel` - 取消任务
- **POST** `/api/queue/tasks/<task_id>/pause` - 暂停任务
- **POST** `/api/queue/tasks/<task_id>/resume` - 恢复任务
- **POST** `/api/queue/tasks/<task_id>/retry` - 重试任务
- **GET** `/api/queue/status` - 获取队列状态
- **POST** `/api/queue/cleanup` - 清理已完成任务

### 数据验证
- **POST** `/api/validation/validate` - 验证装备数据
- **POST** `/api/validation/batch` - 批量验证装备数据
- **GET** `/api/validation/summary` - 获取验证摘要

### 推荐服务
- **GET** `/api/recommendations/price-range` - 价格区间推荐
- **GET** `/api/recommendations/trending` - 热门推荐
- **GET** `/api/recommendations/stats` - 推荐统计

### 价格预警（预留接口，暂未启用）
- **POST** `/api/alerts` - 创建价格预警
- **GET** `/api/alerts/<alert_id>` - 获取预警详情
- **PUT** `/api/alerts/<alert_id>` - 更新预警
- **DELETE** `/api/alerts/<alert_id>` - 删除预警
- **GET** `/api/alerts/user/<user_id>` - 获取用户预警
- **GET** `/api/alerts/history` - 获取预警历史
- **GET** `/api/alerts/stats` - 获取预警统计

## 错误处理

### 常见错误码
- **200** - 成功
- **400** - 请求参数错误
- **403** - 禁止访问（未认证或权限不足）
- **404** - 资源未找到
- **500** - 服务器内部错误
- **503** - 服务不可用（如价格预警服务暂未启用）

### 解决方案
1. **500错误**: 检查对应后端服务是否正常启动
2. **403错误**: 确认JWT Token是否有效，API端点路径是否正确
3. **连接错误**: 检查后端服务是否在指定端口运行

## 前端调用示例

```javascript
// 正确的API调用方式（通过Java后端代理或直连）
const routes = await fetch('/cycling-routes?limit=3').then(r => r.json());

// 调用Python后端API（需处理跨域）
const categories = await fetch('http://localhost:5000/api/equipment/categories')
  .then(r => r.json());

// 提交反馈
const result = await fetch('/feedback', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(feedbackData)
}).then(r => r.json());
```

## 注意事项

1. Java后端API前缀为 `/`（无前缀），Python后端API前缀为 `/api`
2. 认证相关接口（`/user/*`）需要携带JWT Token，格式：`Authorization: Bearer <token>`
3. 确保后端服务在测试前已正确启动
4. 数据库连接配置应与后端保持一致
