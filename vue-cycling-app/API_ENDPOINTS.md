# API 端点说明文档

## Java 后端 API (http://localhost:8080/api)

### 健康检查
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
    "showSteps": true
  }
  ```

- **GET** `/route/quick-plan` - 快速路线规划
  - 查询参数: `origin`, `destination`, `transportMode`, `city`
  - 示例: `/route/quick-plan?origin=起点&destination=终点&transportMode=riding`

### 地理编码服务
- **POST** `/route/geocode` - 地址转坐标
- **POST** `/route/reverse-geocode` - 坐标转地址

### 配置信息
- **GET** `/route/transport-modes` - 获取支持的交通方式
- **GET** `/route/strategies` - 获取路线策略选项

### 数据库测试
- **GET** `/test` - 基本数据库连接测试
- **GET** `/tables` - 获取数据库表列表
- **GET** `/cycling-routes` - 获取骑行路线列表
  - 查询参数: `limit` (可选) - 限制返回数量

### 反馈管理
- **POST** `/feedback` - 创建新反馈
- **GET** `/feedback` - 获取反馈列表
- **GET** `/feedback/{id}` - 获取特定反馈
- **PUT** `/feedback/{id}` - 更新反馈
- **DELETE** `/feedback/{id}` - 删除反馈

## Python 后端 API (http://localhost:5000/api)

### 健康检查
- **GET** `/health` - 检查Python后端服务状态

### 装备分类管理
- **GET** `/equipment/categories` - 获取所有装备分类

### 装备搜索和管理
- **GET** `/equipment/search` - 搜索装备
  - 查询参数:
    - `keyword` - 关键词搜索
    - `category_id` - 分类ID
    - `min_price` - 最低价格
    - `max_price` - 最高价格
    - `platform` - 平台筛选
    - `page` - 页码
    - `per_page` - 每页数量

- **GET** `/equipment` - 获取装备列表
- **POST** `/equipment` - 添加新装备
- **PUT** `/equipment/{id}` - 更新装备信息
- **DELETE** `/equipment/{id}` - 删除装备

### 爬虫服务
- **POST** `/equipment/crawl` - 手动触发爬虫
  - 请求体示例:
  ```json
  {
    "platform": "taobao",
    "category": "helmet"
  }
  ```

- **GET** `/equipment/crawl/status/{task_id}` - 获取爬虫任务状态
- **POST** `/equipment/crawl/stop/{task_id}` - 停止爬虫任务

### 装备推荐
- **GET** `/equipment/recommend` - 获取推荐装备
- **GET** `/equipment/popular` - 获取热门装备
- **GET** `/equipment/price-monitor` - 价格监控

## 错误处理

### 常见错误码
- **500** - 服务器内部错误（通常是后端未启动或配置错误）
- **403** - 禁止访问（API端点不存在或权限不足）
- **404** - 资源未找到
- **400** - 请求参数错误

### 解决方案
1. **500错误**: 检查Java后端是否正常启动
2. **403错误**: 确认API端点路径正确，符合RESTful规范
3. **连接错误**: 检查后端服务是否在指定端口运行

## 前端调用示例

```javascript
// 正确的API调用方式
const routes = await Database.query('/cycling-routes', { limit: 3 });
const feedback = await Database.insert('/feedback', feedbackData);
const result = await Database.delete(`/feedback/${id}`);

// 错误的调用方式（不要这样做）
const routes = await Database.query('SELECT * FROM cycling_routes LIMIT 3');
```

## 注意事项

1. 前端不应直接发送SQL语句到后端
2. 所有API调用都应使用RESTful风格的端点
3. 确保后端服务在测试前已正确启动
4. 数据库连接配置应与后端保持一致