# 灵境行者 - Java后端服务

## 项目简介

灵境行者Java后端服务是基于Spring Boot 3.3.0开发的主要API服务，集成高德地图API，为前端Vue应用提供路径规划、地理编码、用户认证、数据库操作等核心功能。作为项目的主要后端服务，与Python爬虫服务协同工作，共同支撑整个骑行应用生态。

### 数据库集成
- **主数据库**: MySQL 8.0，数据库名：`ljxz`
- **ORM框架**: Spring Data JPA + MyBatis
- **连接池**: HikariCP（Spring Boot默认）
- **数据表**: 用户管理、骑行路线、骑行记录、装备信息等核心业务表
- **事务管理**: 声明式事务

## 🚀 功能特性

### 核心功能
- 🚗 **智能路径规划**：支持驾车、步行、公交、骑行四种交通方式的路线规划
- 🗺️ **地理编码服务**：地址与坐标的双向转换
- 🎯 **多策略路径优化**：速度优先、费用优先、距离优先等多种路径策略
- 🔐 **用户认证系统**：JWT token认证，支持用户注册、登录、刷新Token、权限管理
- 📊 **数据库管理**：骑行路线、用户反馈等数据的查询操作
- 🚀 **高性能缓存**：内置路径规划结果缓存，提升响应速度
- 🔒 **参数验证**：完善的请求参数验证和全局异常处理
- 🌐 **跨域支持**：完整的CORS配置，支持前端跨域访问

### 与其他服务的集成
- **前端集成**：为Vue3前端提供RESTful API接口
- **Python后端协作**：与Python爬虫服务配合，提供完整的装备推荐功能
- **高德地图集成**：深度集成高德地图Web服务API

## 🛠️ 技术栈

- **框架**: Spring Boot 3.3.0
- **数据库**: MySQL 8.0.33
- **ORM**: Spring Data JPA + MyBatis 2.3.1
- **HTTP客户端**: Apache HttpClient 4.5.14
- **JSON处理**: Jackson 2.15.2
- **构建工具**: Maven 3.8+
- **Java版本**: JDK 17
- **安全**: Spring Security + JWT (jjwt 0.11.5)
- **工具**: Lombok 1.18.36

## 快速开始

### 环境要求

- JDK 17
- Maven 3.6+
- MySQL 8.0+

### 安装步骤

1. **进入项目目录**
   ```bash
   cd java-backend
   ```

2. **配置数据库**
   ```sql
   CREATE DATABASE ljxz CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **修改配置文件**
   
   编辑 `src/main/resources/application.yml`，修改数据库连接信息：
   ```yaml
   spring:
     datasource:
       url: jdbc:mysql://localhost:3306/ljxz?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true
       username: your_username
       password: your_password
   ```

4. **配置高德地图API**
   
   在 `application.yml` 中配置你的高德地图API密钥：
   ```yaml
   amap:
     web-api-key: your_web_api_key
     js-api-key: your_js_api_key
     security-key: your_security_key
   ```

5. **编译运行**
   ```bash
   mvn clean install
   mvn spring-boot:run
   ```

6. **验证服务**
   
   访问 http://localhost:8080/health 或 http://localhost:8080/route/health 检查服务状态

## API文档

### 基础信息

- **基础URL**: `http://localhost:8080`
- **Content-Type**: `application/json`

### 主要接口

#### 1. 路径规划（完整参数）

**POST** `/route/plan`

请求体示例：
```json
{
  "origin": "石家庄市长安区",
  "destination": "石家庄市裕华区",
  "transportMode": "driving",
  "city": "石家庄",
  "strategy": 0,
  "showSteps": true,
  "waypoints": ["石家庄市桥西区"]
}
```

#### 2. 快速路径规划（简化参数）

**GET** `/route/quick-plan`

参数：
- `origin`: 起点（必需）
- `destination`: 终点（必需）
- `transportMode`: 交通方式（必需）
- `city`: 城市（可选）

示例：
```
GET /route/quick-plan?origin=石家庄市长安区&destination=石家庄市裕华区&transportMode=driving&city=石家庄
```

#### 3. 地理编码（地址转坐标）

**GET** `/route/geocode`

参数：
- `address`: 地址（必需）
- `city`: 城市（可选）

#### 4. 逆地理编码（坐标转地址）

**GET** `/route/reverse-geocode`

参数：
- `longitude`: 经度（必需）
- `latitude`: 纬度（必需）

#### 5. 获取支持的交通方式

**GET** `/route/transport-modes`

#### 6. 获取路径规划策略

**GET** `/route/strategies`

#### 7. 用户认证

**POST** `/auth/login` - 用户登录
**POST** `/auth/register` - 用户注册
**POST** `/auth/refresh` - 刷新Token
**POST** `/auth/logout` - 用户登出
**GET** `/auth/check-username` - 检查用户名
**GET** `/auth/check-email` - 检查邮箱

#### 8. 用户管理

**GET** `/user/profile` - 获取当前用户信息（需JWT认证）
**PUT** `/user/profile` - 更新用户信息（需JWT认证）
**GET** `/user/records` - 获取用户记录（需JWT认证）

#### 9. 其他接口

**GET** `/health`, `/route/health` - 健康检查
**GET** `/test` - 测试接口
**GET** `/tables` - 数据库表列表
**GET** `/cycling-routes` - 骑行路线列表（模拟数据）
**POST** `/feedback` - 提交反馈
**GET** `/docs` - API文档说明

### 响应格式

所有接口统一返回格式：
```json
{
  "status": 1,
  "message": "路径规划成功",
  "route": {
    "origin": {
      "longitude": 114.502461,
      "latitude": 38.045474,
      "address": "石家庄市长安区"
    },
    "destination": {
      "longitude": 114.522461,
      "latitude": 38.065474,
      "address": "石家庄市裕华区"
    },
    "distance": 5000,
    "duration": 900,
    "cost": 0.0,
    "trafficLights": 5,
    "polyline": "encoded_polyline_string",
    "transportMode": "driving",
    "steps": [
      {
        "stepIndex": 1,
        "instruction": "向东行驶",
        "roadName": "中山路",
        "distance": 1000,
        "duration": 180,
        "action": "直行"
      }
    ]
  },
  "timestamp": "2024-01-01 12:00:00",
  "processingTime": 150
}
```

## 交通方式说明

| 代码 | 名称 | 说明 |
|------|------|------|
| driving | 驾车 | 适用于汽车出行，提供最优驾车路线 |
| walking | 步行 | 适用于步行出行，提供步行路线 |
| transit | 公交 | 适用于公共交通出行，包括公交、地铁等 |
| riding | 骑行 | 适用于自行车出行，提供骑行路线 |

## 路径策略说明

| 代码 | 名称 | 说明 |
|------|------|------|
| 0 | 速度优先 | 时间最短路线 |
| 1 | 费用优先 | 费用最少路线 |
| 2 | 距离优先 | 距离最短路线 |
| 3 | 不走快速路 | 避开快速路的路线 |
| 4 | 躲避拥堵 | 避开拥堵路段 |
| 5 | 多策略 | 综合速度、费用、距离的路线 |

## 错误码说明

| 状态码 | 说明 |
|--------|------|
| 1 | 成功 |
| 0 | 失败 |

## 配置说明

### 高德地图配置

```yaml
amap:
  web-api-key: your_web_api_key      # Web服务API Key
  js-api-key: your_js_api_key        # Web端JS API Key
  security-key: your_security_key    # 安全密钥
  base-url: https://restapi.amap.com/v3  # API基础URL
  timeout: 10000                     # 请求超时时间(毫秒)
  retry-count: 3                     # 重试次数
```

### 路径规划配置

```yaml
route:
  default-city: 石家庄               # 默认城市
  max-waypoints: 16                 # 最大路径点数
  cache-expire-minutes: 30          # 缓存过期时间(分钟)
```

### JWT配置

```yaml
jwt:
  secret: your-secret-key
  expiration: 86400000              # Token过期时间(ms)，默认24小时
```

## 部署说明

### Docker部署

1. **构建镜像**
   ```bash
   mvn clean package
   docker build -t ljxz-java-backend .
   ```

2. **运行容器**
   ```bash
   docker run -d -p 8080:8080 \
     -e SPRING_DATASOURCE_URL=jdbc:mysql://host:3306/ljxz \
     -e SPRING_DATASOURCE_USERNAME=username \
     -e SPRING_DATASOURCE_PASSWORD=password \
     -e AMAP_WEB_API_KEY=your_api_key \
     ljxz-java-backend
   ```

### 生产环境配置

1. **JVM参数优化**
   ```bash
   java -Xms512m -Xmx1024m -XX:+UseG1GC -jar cycling-route-backend-1.0.0.jar
   ```

2. **日志配置**
   
   生产环境建议修改日志级别：
   ```yaml
   logging:
     level:
       com.ljxz.cycling: INFO
       org.springframework.web: WARN
   ```

## 性能优化

1. **缓存策略**：内置内存缓存，生产环境建议使用Redis
2. **连接池**：配置了HikariCP连接池，可根据需要调整参数
3. **HTTP客户端**：使用Apache HttpClient连接池，支持重试机制
4. **异步处理**：可考虑引入异步处理提升并发性能

## 代码结构

```
src/main/java/com/ljxz/cycling/
├── CyclingRouteApplication.java    # 启动类
├── controller/                     # 控制器层
│   ├── RouteController.java        # 路线规划、地理编码、健康检查
│   ├── AuthController.java         # 用户认证（登录、注册、刷新Token）
│   └── UserController.java         # 用户管理（资料、记录）
├── service/                        # 服务层
│   ├── RouteService.java           # 路线规划业务逻辑
│   ├── AmapService.java            # 高德地图API调用
│   ├── AuthService.java            # 认证业务逻辑
│   ├── UserService.java            # 用户业务逻辑
│   └── UserDetailsServiceImpl.java # Spring Security用户详情
├── entity/                         # 实体类
│   ├── RouteRequest.java           # 路线规划请求
│   ├── RouteResponse.java          # 路线规划响应
│   └── User.java                   # 用户实体
├── dto/                            # 数据传输对象
│   ├── LoginRequest.java
│   ├── RegisterRequest.java
│   └── RefreshTokenRequest.java
├── repository/                     # 数据访问层
│   └── UserRepository.java
├── config/                         # 配置类
│   ├── WebConfig.java              # Web配置（CORS等）
│   ├── SecurityConfig.java         # Spring Security配置
│   ├── JwtAuthenticationFilter.java # JWT认证过滤器
│   └── GlobalExceptionHandler.java # 全局异常处理
├── util/                           # 工具类
│   └── JwtUtil.java                # JWT工具类
└── resources/
    └── application.yml             # 应用配置文件
```

## 扩展开发

1. **添加新的交通方式**：在AmapService中添加对应的API端点
2. **集成其他地图服务**：实现新的地图服务类，遵循相同的接口规范
3. **添加缓存**：可集成Redis替换内存缓存
4. **添加新功能**：在controller和service层添加新的业务模块

## 常见问题

### Q1: 高德API调用失败
**A**: 检查API密钥是否正确，确保账户有足够的调用配额

### Q2: 数据库连接失败
**A**: 检查数据库连接配置，确保数据库服务正常运行

### Q3: 跨域问题
**A**: 项目已配置CORS支持，如仍有问题请检查前端请求配置

### Q4: 路径规划结果为空
**A**: 检查起终点地址是否正确，确保在高德地图支持的范围内

### Q5: JWT认证失败
**A**: 检查Token是否过期，确认请求头中正确携带 `Authorization: Bearer <token>`

## 许可证

MIT License

## 联系方式

- 项目地址：[GitHub Repository]
- 问题反馈：[Issues]

---

**河北经贸大学/陈冠衡/灵境行者** © 2025
