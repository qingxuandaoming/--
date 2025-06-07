# API 端点说明文档

## Java 后端 API (http://localhost:8080/api)

### 健康检查
- **GET** `/route/health` - 检查后端服务状态

### 数据库测试
- **GET** `/test` - 基本数据库连接测试
- **GET** `/tables` - 获取数据库表列表

### 骑行路线
- **GET** `/cycling-routes` - 获取骑行路线列表
  - 查询参数: `limit` (可选) - 限制返回数量
  - 示例: `/cycling-routes?limit=3`

### 反馈管理
- **POST** `/feedback` - 创建新反馈
- **GET** `/feedback` - 获取反馈列表
- **GET** `/feedback/{id}` - 获取特定反馈
- **PUT** `/feedback/{id}` - 更新反馈
- **DELETE** `/feedback/{id}` - 删除反馈

## Python 后端 API (http://localhost:5000/api)

### 爬虫服务
- **GET** `/crawler/status` - 获取爬虫状态
- **POST** `/crawler/start` - 启动爬虫
- **POST** `/crawler/stop` - 停止爬虫

### 设备管理
- **GET** `/equipment` - 获取设备列表
- **POST** `/equipment` - 添加新设备
- **PUT** `/equipment/{id}` - 更新设备信息
- **DELETE** `/equipment/{id}` - 删除设备

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