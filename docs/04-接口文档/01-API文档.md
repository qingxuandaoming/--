# 灵境行者 - API 文档

## 📋 目录

- [API 概览](#api-概览)
- [认证机制](#认证机制)
- [通用响应格式](#通用响应格式)
- [错误处理](#错误处理)
- [Java 后端 API](#java-后端-api)
- [Python 后端 API](#python-后端-api)
- [API 测试](#api-测试)
- [版本管理](#版本管理)

## 🌐 API 概览

### 服务架构

```
前端应用 (Vue 3)
    ↓
┌─────────────────┬─────────────────┐
│   Java 后端     │   Python 后端   │
│   (端口: 8080)   │   (端口: 5000)   │
│                 │                 │
│ • 用户管理       │ • 设备数据爬取   │
│ • 路线规划       │ • 数据处理      │
│ • 数据存储       │ • 外部API集成   │
└─────────────────┴─────────────────┘
    ↓
MySQL 数据库 (端口: 3306)
```

### 服务端点

| 服务 | 基础URL | 端口 | 状态检查 | API文档 |
|------|---------|------|----------|----------|
| Java 后端 | `http://localhost:8080` | 8080 | `/actuator/health` | `/swagger-ui.html` |
| Python 后端 | `http://localhost:5000` | 5000 | `/health` | `/docs` |
| 前端应用 | `http://localhost:5174` | 5174 | - | - |

## 🔐 认证机制

### JWT Token 认证

```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

### 获取 Token

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password123"
}
```

**响应：**

```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "refresh_token_here",
    "expiresIn": 3600,
    "user": {
      "id": 1,
      "username": "user@example.com",
      "nickname": "用户昵称",
      "avatar": "avatar_url"
    }
  }
}
```

### Token 刷新

```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refreshToken": "refresh_token_here"
}
```

## 📄 通用响应格式

### 成功响应

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    // 具体数据
  },
  "timestamp": "2025-01-01T12:00:00Z"
}
```

### 分页响应

```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "content": [
      // 数据列表
    ],
    "page": {
      "current": 1,
      "size": 20,
      "total": 100,
      "totalPages": 5
    }
  },
  "timestamp": "2025-01-01T12:00:00Z"
}
```

## ❌ 错误处理

### HTTP 状态码

| 状态码 | 说明 | 示例场景 |
|--------|------|----------|
| 200 | 成功 | 请求处理成功 |
| 201 | 创建成功 | 资源创建成功 |
| 400 | 请求错误 | 参数验证失败 |
| 401 | 未授权 | Token 无效或过期 |
| 403 | 禁止访问 | 权限不足 |
| 404 | 资源不存在 | 请求的资源未找到 |
| 500 | 服务器错误 | 内部服务器错误 |

### 错误响应格式

```json
{
  "code": 400,
  "message": "请求参数错误",
  "error": {
    "type": "VALIDATION_ERROR",
    "details": [
      {
        "field": "email",
        "message": "邮箱格式不正确"
      },
      {
        "field": "password",
        "message": "密码长度至少6位"
      }
    ]
  },
  "timestamp": "2025-01-01T12:00:00Z"
}
```

## ☕ Java 后端 API

### 用户管理

#### 用户注册

```http
POST /api/users/register
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password123",
  "nickname": "用户昵称",
  "phone": "13800138000"
}
```

**响应：**

```json
{
  "code": 201,
  "message": "注册成功",
  "data": {
    "id": 1,
    "username": "user@example.com",
    "nickname": "用户昵称",
    "phone": "13800138000",
    "avatar": null,
    "createdAt": "2025-01-01T12:00:00Z"
  }
}
```

#### 获取用户信息

```http
GET /api/users/{id}
Authorization: Bearer <jwt_token>
```

**响应：**

```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "id": 1,
    "username": "user@example.com",
    "nickname": "用户昵称",
    "phone": "13800138000",
    "avatar": "avatar_url",
    "createdAt": "2025-01-01T12:00:00Z",
    "updatedAt": "2025-01-01T12:00:00Z"
  }
}
```

#### 更新用户信息

```http
PUT /api/users/{id}
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "nickname": "新昵称",
  "phone": "13900139000",
  "avatar": "new_avatar_url"
}
```

#### 用户列表

```http
GET /api/users?page=1&size=20&keyword=搜索关键词
Authorization: Bearer <jwt_token>
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| size | int | 否 | 每页大小，默认20 |
| keyword | string | 否 | 搜索关键词 |
| status | string | 否 | 用户状态：active/inactive |

### 路线管理

#### 创建路线

```http
POST /api/routes
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "name": "西湖环线",
  "description": "杭州西湖骑行路线",
  "startPoint": {
    "latitude": 30.2741,
    "longitude": 120.1551,
    "address": "杭州市西湖区"
  },
  "endPoint": {
    "latitude": 30.2441,
    "longitude": 120.1351,
    "address": "杭州市西湖区"
  },
  "waypoints": [
    {
      "latitude": 30.2641,
      "longitude": 120.1451,
      "address": "中间点1"
    }
  ],
  "difficulty": "EASY",
  "estimatedTime": 120,
  "distance": 15.5,
  "tags": ["风景", "休闲"]
}
```

**响应：**

```json
{
  "code": 201,
  "message": "路线创建成功",
  "data": {
    "id": 1,
    "name": "西湖环线",
    "description": "杭州西湖骑行路线",
    "startPoint": {
      "latitude": 30.2741,
      "longitude": 120.1551,
      "address": "杭州市西湖区"
    },
    "endPoint": {
      "latitude": 30.2441,
      "longitude": 120.1351,
      "address": "杭州市西湖区"
    },
    "waypoints": [...],
    "difficulty": "EASY",
    "estimatedTime": 120,
    "distance": 15.5,
    "tags": ["风景", "休闲"],
    "createdBy": 1,
    "createdAt": "2025-01-01T12:00:00Z"
  }
}
```

#### 获取路线列表

```http
GET /api/routes?page=1&size=20&difficulty=EASY&tag=风景
Authorization: Bearer <jwt_token>
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| size | int | 否 | 每页大小，默认20 |
| difficulty | string | 否 | 难度：EASY/MEDIUM/HARD |
| tag | string | 否 | 标签筛选 |
| minDistance | double | 否 | 最小距离 |
| maxDistance | double | 否 | 最大距离 |
| city | string | 否 | 城市筛选 |

#### 获取路线详情

```http
GET /api/routes/{id}
Authorization: Bearer <jwt_token>
```

#### 更新路线

```http
PUT /api/routes/{id}
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "name": "更新后的路线名称",
  "description": "更新后的描述"
}
```

#### 删除路线

```http
DELETE /api/routes/{id}
Authorization: Bearer <jwt_token>
```

### 路线规划

#### 智能路线规划

```http
POST /api/routes/plan
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "startPoint": {
    "latitude": 30.2741,
    "longitude": 120.1551
  },
  "endPoint": {
    "latitude": 30.2441,
    "longitude": 120.1351
  },
  "preferences": {
    "avoidHighways": true,
    "preferScenic": true,
    "maxDistance": 50,
    "difficulty": "MEDIUM"
  }
}
```

**响应：**

```json
{
  "code": 200,
  "message": "路线规划成功",
  "data": {
    "routes": [
      {
        "id": "route_1",
        "name": "推荐路线1",
        "distance": 15.5,
        "estimatedTime": 120,
        "difficulty": "MEDIUM",
        "coordinates": [
          [120.1551, 30.2741],
          [120.1451, 30.2641],
          [120.1351, 30.2441]
        ],
        "instructions": [
          {
            "step": 1,
            "instruction": "从起点出发，向南行驶",
            "distance": 500,
            "duration": 120
          }
        ],
        "elevation": [
          {"distance": 0, "elevation": 10},
          {"distance": 1000, "elevation": 25}
        ]
      }
    ]
  }
}
```

### 骑行记录

#### 开始骑行

```http
POST /api/rides/start
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "routeId": 1,
  "startLocation": {
    "latitude": 30.2741,
    "longitude": 120.1551
  }
}
```

#### 更新骑行位置

```http
PUT /api/rides/{rideId}/location
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "latitude": 30.2641,
  "longitude": 120.1451,
  "timestamp": "2025-01-01T12:30:00Z",
  "speed": 15.5,
  "altitude": 25.0
}
```

#### 结束骑行

```http
POST /api/rides/{rideId}/finish
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "endLocation": {
    "latitude": 30.2441,
    "longitude": 120.1351
  },
  "totalDistance": 15.5,
  "totalTime": 3600,
  "averageSpeed": 15.5,
  "maxSpeed": 25.0,
  "calories": 450
}
```

#### 获取骑行记录

```http
GET /api/rides?page=1&size=20&startDate=2025-01-01&endDate=2025-01-31
Authorization: Bearer <jwt_token>
```

### 设备管理

#### 绑定设备

```http
POST /api/devices/bind
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "deviceId": "device_123",
  "deviceType": "BIKE_COMPUTER",
  "deviceName": "我的码表",
  "manufacturer": "Garmin",
  "model": "Edge 530"
}
```

#### 获取设备列表

```http
GET /api/devices
Authorization: Bearer <jwt_token>
```

#### 设备数据同步

```http
POST /api/devices/{deviceId}/sync
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "data": {
    "rides": [...],
    "heartRate": [...],
    "power": [...]
  }
}
```

## 🐍 Python 后端 API

### 设备数据爬取

#### 获取设备信息

```http
GET /api/equipment?page=1&limit=20&category=自行车
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| limit | int | 否 | 每页大小，默认20 |
| category | string | 否 | 设备类别 |
| brand | string | 否 | 品牌筛选 |
| minPrice | float | 否 | 最低价格 |
| maxPrice | float | 否 | 最高价格 |

**响应：**

```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "捷安特 ATX 810",
        "category": "山地车",
        "brand": "捷安特",
        "price": 2998.0,
        "originalPrice": 3298.0,
        "discount": 0.91,
        "description": "入门级山地车，适合城市骑行",
        "specifications": {
          "frame": "铝合金",
          "wheelSize": "26寸",
          "gears": "21速",
          "weight": "13.5kg"
        },
        "images": [
          "https://example.com/image1.jpg",
          "https://example.com/image2.jpg"
        ],
        "availability": true,
        "stock": 15,
        "rating": 4.5,
        "reviewCount": 128,
        "source": "京东",
        "sourceUrl": "https://item.jd.com/12345.html",
        "lastUpdated": "2025-01-01T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "totalPages": 8
    }
  }
}
```

#### 获取设备详情

```http
GET /api/equipment/{id}
```

**响应：**

```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "id": 1,
    "name": "捷安特 ATX 810",
    "category": "山地车",
    "brand": "捷安特",
    "price": 2998.0,
    "originalPrice": 3298.0,
    "discount": 0.91,
    "description": "入门级山地车，适合城市骑行和轻度越野",
    "detailedDescription": "详细的产品描述...",
    "specifications": {
      "frame": "铝合金车架",
      "fork": "前叉避震",
      "wheelSize": "26寸",
      "gears": "21速变速系统",
      "brakes": "V刹",
      "weight": "13.5kg",
      "maxLoad": "120kg"
    },
    "images": [
      "https://example.com/image1.jpg",
      "https://example.com/image2.jpg",
      "https://example.com/image3.jpg"
    ],
    "availability": true,
    "stock": 15,
    "rating": 4.5,
    "reviewCount": 128,
    "reviews": [
      {
        "id": 1,
        "user": "用户A",
        "rating": 5,
        "comment": "性价比很高，骑行体验不错",
        "date": "2025-01-01T10:00:00Z"
      }
    ],
    "relatedProducts": [
      {
        "id": 2,
        "name": "相关产品",
        "price": 1998.0,
        "image": "https://example.com/related1.jpg"
      }
    ],
    "priceHistory": [
      {
        "date": "2024-12-01",
        "price": 3298.0
      },
      {
        "date": "2025-01-01",
        "price": 2998.0
      }
    ],
    "source": "京东",
    "sourceUrl": "https://item.jd.com/12345.html",
    "lastUpdated": "2025-01-01T12:00:00Z"
  }
}
```

#### 搜索设备

```http
GET /api/equipment/search?q=山地车&category=自行车&minPrice=1000&maxPrice=5000
```

**查询参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | 是 | 搜索关键词 |
| category | string | 否 | 设备类别 |
| brand | string | 否 | 品牌筛选 |
| minPrice | float | 否 | 最低价格 |
| maxPrice | float | 否 | 最高价格 |
| sortBy | string | 否 | 排序字段：price/rating/sales |
| sortOrder | string | 否 | 排序方向：asc/desc |

#### 获取品牌列表

```http
GET /api/equipment/brands?category=自行车
```

**响应：**

```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    {
      "name": "捷安特",
      "count": 45,
      "logo": "https://example.com/giant-logo.png"
    },
    {
      "name": "美利达",
      "count": 32,
      "logo": "https://example.com/merida-logo.png"
    }
  ]
}
```

#### 获取类别列表

```http
GET /api/equipment/categories
```

**响应：**

```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    {
      "name": "自行车",
      "count": 150,
      "subcategories": [
        {"name": "山地车", "count": 60},
        {"name": "公路车", "count": 45},
        {"name": "折叠车", "count": 25},
        {"name": "电动车", "count": 20}
      ]
    },
    {
      "name": "骑行装备",
      "count": 80,
      "subcategories": [
        {"name": "头盔", "count": 25},
        {"name": "骑行服", "count": 30},
        {"name": "手套", "count": 15},
        {"name": "眼镜", "count": 10}
      ]
    }
  ]
}
```

### 数据爬取管理

#### 触发数据爬取

```http
POST /api/crawler/start
Content-Type: application/json

{
  "sources": ["jd", "tmall", "taobao"],
  "categories": ["自行车", "骑行装备"],
  "maxPages": 10,
  "updateExisting": true
}
```

**响应：**

```json
{
  "code": 200,
  "message": "爬取任务已启动",
  "data": {
    "taskId": "task_123456",
    "status": "RUNNING",
    "startTime": "2025-01-01T12:00:00Z",
    "estimatedDuration": 1800
  }
}
```

#### 获取爬取任务状态

```http
GET /api/crawler/tasks/{taskId}
```

**响应：**

```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "taskId": "task_123456",
    "status": "RUNNING",
    "progress": {
      "current": 150,
      "total": 500,
      "percentage": 30
    },
    "startTime": "2025-01-01T12:00:00Z",
    "estimatedEndTime": "2025-01-01T12:30:00Z",
    "results": {
      "newItems": 45,
      "updatedItems": 105,
      "errors": 2
    },
    "logs": [
      {
        "timestamp": "2025-01-01T12:05:00Z",
        "level": "INFO",
        "message": "开始爬取京东数据"
      },
      {
        "timestamp": "2025-01-01T12:10:00Z",
        "level": "WARNING",
        "message": "某个商品页面访问失败"
      }
    ]
  }
}
```

#### 停止爬取任务

```http
POST /api/crawler/tasks/{taskId}/stop
```

#### 获取爬取历史

```http
GET /api/crawler/history?page=1&limit=20
```

### 数据统计

#### 获取统计信息

```http
GET /api/stats/overview
```

**响应：**

```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "totalEquipment": 1250,
    "totalBrands": 45,
    "totalCategories": 8,
    "lastUpdateTime": "2025-01-01T12:00:00Z",
    "categoryStats": [
      {
        "category": "自行车",
        "count": 800,
        "avgPrice": 2500.0
      },
      {
        "category": "骑行装备",
        "count": 450,
        "avgPrice": 150.0
      }
    ],
    "priceRangeStats": [
      {"range": "0-500", "count": 200},
      {"range": "500-1000", "count": 300},
      {"range": "1000-3000", "count": 500},
      {"range": "3000+", "count": 250}
    ]
  }
}
```

### 健康检查

#### 服务状态检查

```http
GET /health
```

**响应：**

```json
{
  "status": "healthy",
  "timestamp": "2025-01-01T12:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "crawler": "healthy"
  },
  "metrics": {
    "uptime": 86400,
    "memoryUsage": "45%",
    "cpuUsage": "12%",
    "activeConnections": 15
  }
}
```

## 🧪 API 测试

### 使用 curl 测试

#### 测试用户注册

```bash
curl -X POST http://localhost:8080/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test@example.com",
    "password": "password123",
    "nickname": "测试用户"
  }'
```

#### 测试用户登录

```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test@example.com",
    "password": "password123"
  }'
```

#### 测试获取设备列表

```bash
curl -X GET "http://localhost:5000/api/equipment?page=1&limit=10&category=自行车"
```

### 使用 Postman 测试

#### 环境变量设置

```json
{
  "java_base_url": "http://localhost:8080",
  "python_base_url": "http://localhost:5000",
  "jwt_token": "{{token}}"
}
```

#### 预请求脚本（获取 Token）

```javascript
// 在需要认证的请求中添加此预请求脚本
if (!pm.environment.get("jwt_token")) {
    pm.sendRequest({
        url: pm.environment.get("java_base_url") + "/api/auth/login",
        method: 'POST',
        header: {
            'Content-Type': 'application/json'
        },
        body: {
            mode: 'raw',
            raw: JSON.stringify({
                username: "test@example.com",
                password: "password123"
            })
        }
    }, function (err, response) {
        if (response.json().data.token) {
            pm.environment.set("jwt_token", response.json().data.token);
        }
    });
}
```

### 自动化测试脚本

#### Python 测试脚本

```python
#!/usr/bin/env python3
# test_api.py

import requests
import json
import time

class APITester:
    def __init__(self):
        self.java_base_url = "http://localhost:8080"
        self.python_base_url = "http://localhost:5000"
        self.token = None
    
    def login(self, username="test@example.com", password="password123"):
        """用户登录获取 Token"""
        response = requests.post(
            f"{self.java_base_url}/api/auth/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            self.token = response.json()["data"]["token"]
            print("✅ 登录成功")
            return True
        else:
            print("❌ 登录失败")
            return False
    
    def get_headers(self):
        """获取请求头"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def test_user_apis(self):
        """测试用户相关 API"""
        print("\n🧪 测试用户 API...")
        
        # 测试获取用户信息
        response = requests.get(
            f"{self.java_base_url}/api/users/1",
            headers=self.get_headers()
        )
        if response.status_code == 200:
            print("✅ 获取用户信息成功")
        else:
            print("❌ 获取用户信息失败")
    
    def test_equipment_apis(self):
        """测试设备相关 API"""
        print("\n🧪 测试设备 API...")
        
        # 测试获取设备列表
        response = requests.get(
            f"{self.python_base_url}/api/equipment?page=1&limit=5"
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取设备列表成功，共 {len(data['data']['items'])} 条记录")
        else:
            print("❌ 获取设备列表失败")
    
    def test_health_checks(self):
        """测试健康检查"""
        print("\n🧪 测试健康检查...")
        
        # Java 后端健康检查
        try:
            response = requests.get(f"{self.java_base_url}/actuator/health")
            if response.status_code == 200:
                print("✅ Java 后端健康检查通过")
            else:
                print("❌ Java 后端健康检查失败")
        except requests.exceptions.ConnectionError:
            print("❌ Java 后端连接失败")
        
        # Python 后端健康检查
        try:
            response = requests.get(f"{self.python_base_url}/health")
            if response.status_code == 200:
                print("✅ Python 后端健康检查通过")
            else:
                print("❌ Python 后端健康检查失败")
        except requests.exceptions.ConnectionError:
            print("❌ Python 后端连接失败")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始 API 测试...")
        
        # 健康检查
        self.test_health_checks()
        
        # 登录
        if self.login():
            # 测试各个模块
            self.test_user_apis()
            self.test_equipment_apis()
        
        print("\n🎉 测试完成！")

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()
```

## 📋 版本管理

### API 版本策略

| 版本 | 路径前缀 | 状态 | 说明 |
|------|----------|------|------|
| v1 | `/api/v1` | 开发中 | 当前开发版本 |
| v2 | `/api/v2` | 计划中 | 下一个主要版本 |

### 版本兼容性

- **向后兼容**：新版本保持对旧版本的兼容
- **废弃通知**：提前3个月通知 API 废弃
- **迁移指南**：提供详细的版本迁移文档

### 变更日志

#### v1.0.0 (2025-01-01)

**新增功能：**
- 用户注册和登录
- JWT 认证机制
- 路线管理 CRUD
- 设备数据爬取
- 基础统计功能

**API 变更：**
- 初始版本发布

---

## 📞 技术支持

- **API 文档**：访问 Swagger UI 查看交互式文档
- **问题反馈**：通过 GitHub Issues 报告问题
- **技术讨论**：加入项目技术群组

---

*最后更新：2025年1月*