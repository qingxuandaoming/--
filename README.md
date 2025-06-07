# 灵境行者 (Spirit Journey Rider)

## 项目简介

灵境行者是一个现代化的智能骑行应用平台，致力于为骑行爱好者提供全方位的骑行体验。项目采用前后端分离的微服务架构，集成了路径规划、装备推荐、社区互动等核心功能，为用户打造一站式的骑行服务生态。

## 🏗️ 项目架构

```
灵境行者项目
├── vue-cycling-app/     # 前端Vue3应用
├── java-backend/        # Java主后端服务 (Spring Boot)
├── python-backend/      # Python爬虫服务 (Flask)
└── start-java.ps1      # Java服务启动脚本
```

### 架构设计

- **前端层**: Vue3 + Element Plus + 高德地图JS API
- **API网关层**: Java Spring Boot (主服务) + Python Flask (爬虫服务)
- **数据层**: MySQL 8.0 (主数据库) + 内存缓存
- **外部服务**: 高德地图API、电商平台数据源

## 🚀 核心功能

### 🗺️ 智能路径规划
- 支持驾车、步行、公交、骑行四种交通方式
- 多种路径策略：速度优先、费用优先、距离优先
- 实时路况信息和路径优化
- 地理编码和逆地理编码服务

### 🛒 装备推荐系统
- 多平台骑行装备数据爬取（淘宝、京东等）
- 智能搜索和价格比较
- 个性化装备推荐
- 价格趋势分析

### 👥 用户系统
- 用户注册、登录、权限管理
- 个人骑行记录管理
- 路线收藏和评分
- 用户反馈系统

### 📱 现代化界面
- 响应式设计，支持多设备访问
- 直观的地图交互界面
- 实时数据展示和可视化
- 优秀的用户体验设计

## 🛠️ 技术栈

### 前端技术
- **框架**: Vue 3.x + Composition API
- **UI库**: Element Plus
- **地图**: 高德地图JavaScript API
- **路由**: Vue Router 4.x
- **状态管理**: Pinia
- **构建工具**: Vite
- **HTTP客户端**: Axios

### 后端技术
- **Java服务**: Spring Boot 3.x + Spring Data JPA
- **Python服务**: Flask + SQLAlchemy
- **数据库**: MySQL 8.0
- **缓存**: 内存缓存（可扩展Redis）
- **爬虫**: Selenium + BeautifulSoup
- **API文档**: Spring Boot Actuator

### 开发工具
- **版本控制**: Git
- **IDE**: VS Code / IntelliJ IDEA
- **包管理**: npm (前端) + Maven (Java) + pip (Python)
- **容器化**: Docker (可选)

## 🚀 快速开始

### 环境要求

- **Node.js**: 16.x 或更高版本
- **Java**: JDK 17 或更高版本
- **Python**: 3.8 或更高版本
- **MySQL**: 8.0 或更高版本
- **Chrome**: 用于爬虫服务的WebDriver

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd site
   ```

2. **数据库设置**
   ```sql
   CREATE DATABASE cycling_app;
   -- 导入 vue-cycling-app/init.sql
   ```

3. **启动Java后端服务**
   ```bash
   cd java-backend
   mvn clean install
   mvn spring-boot:run
   # 或使用提供的脚本: .\start-java.ps1
   ```

4. **启动Python爬虫服务**
   ```bash
   cd python-backend
   pip install -r requirements.txt
   python app.py
   ```

5. **启动前端应用**
   ```bash
   cd vue-cycling-app
   npm install
   npm run dev
   ```

### 配置说明

#### 高德地图API配置
- 在 `java-backend/src/main/resources/application.yml` 中配置高德地图API密钥
- 在 `vue-cycling-app/src/config/map.js` 中配置前端地图API密钥

#### 数据库配置
- Java后端: `application.yml` 中的数据库连接配置
- Python后端: `config.py` 中的数据库连接配置

## 📚 文档链接

- [前端应用文档](./vue-cycling-app/README.md)
- [Java后端文档](./java-backend/README.md)
- [Python爬虫服务文档](./python-backend/README.md)
- [API接口文档](./vue-cycling-app/API_ENDPOINTS.md)
- [数据库设置指南](./vue-cycling-app/DATABASE_SETUP.md)

## 🌐 服务端口

- **前端应用**: http://localhost:5173
- **Java后端**: http://localhost:8080
- **Python后端**: http://localhost:5000

## 🔧 开发指南

### 代码规范
- 前端遵循Vue3官方风格指南
- Java后端遵循Spring Boot最佳实践
- Python后端遵循PEP 8规范

### 提交规范
- 使用语义化提交信息
- 功能开发使用feature分支
- 代码审查后合并到主分支

### 测试
- 前端: 使用Vitest进行单元测试
- Java后端: 使用JUnit 5进行单元和集成测试
- Python后端: 使用pytest进行测试

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系我们

- 项目维护者: [河北经贸大学/陈冠衡]
- 邮箱: [925342921@qq.com]
- 项目地址: [GitHub仓库地址]

---

**灵境行者** - 让每一次骑行都成为一场精彩的旅程！ 🚴‍♂️✨