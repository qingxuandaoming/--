# AGENTS.md — 灵境行者 (Spirit Journey Rider)

> 本文档面向 AI 编程助手。如果你正在阅读此文件，说明你需要在「灵境行者」项目中进行代码修改、功能开发或问题排查。本文档基于项目实际代码与配置文件编写，所有信息均可追溯至具体文件。

---

## 1. 项目概览

**灵境行者**（全称：非遗骑行导览系统 / Intangible Cultural Heritage Cycling Tour）是一款面向骑行爱好者的智能路线规划与装备推荐平台。

- **核心功能**：
  - 基于高德地图 API 的多策略路径规划（驾车、步行、公交、骑行）
  - 电商平台骑行装备数据爬取（淘宝、京东等）与智能推荐
  - 价格趋势分析可视化（Chart.js）
  - 用户注册/登录、JWT 认证、路线收藏与评分
  - 非遗文化地图展示

- **项目架构**：前后端分离的微服务架构
  - `vue-cycling-app/` — Vue 3 前端应用（端口 5173 或 5500+）
  - `java-backend/` — Java 主后端服务（Spring Boot，端口 8080）
  - `python-backend/` — Python 爬虫与数据分析服务（Flask，端口 5000）
  - `database/` — 数据库初始化脚本
  - `launcher/` — PyInstaller 打包的一键启动器（含 MariaDB 捆绑包）
  - `docs/` — 项目文档（7 个章节，中文撰写）

---

## 2. 技术栈与版本要求

| 组件 | 技术/版本 | 说明 |
|------|-----------|------|
| 前端 | Vue 3.5 + Vite 6.2 + Vue Router 4.5 | 无 Pinia 实际使用（项目已配置但未在 package.json 中列出） |
| 前端 UI | Element Plus（通过 CDN 引入） | 未在 package.json 中显式依赖 |
| 前端图表 | Chart.js 4.4 + vue-chartjs 5.3 | 装备数据可视化 |
| 前端 HTTP | Axios 1.9 | 同时对接 Java 和 Python 两个后端 |
| Java 后端 | Spring Boot 3.3 + JDK 17 + Maven 3.9 | 主业务服务 |
| Java ORM | Spring Data JPA + Hibernate | `ddl-auto: update`，MySQL8Dialect |
| Java 安全 | Spring Security + JWT (jjwt 0.11.5) + BCrypt | 见 `application.yml` 中 `jwt.secret` 和 `security.permit-all` |
| Python 后端 | Flask 2.3 + Flask-SQLAlchemy 3.0 + PyMySQL 1.1 | 爬虫与装备服务 |
| Python 爬虫 | Selenium 4.11 + BeautifulSoup 4.12 + webdriver-manager | 依赖 Chrome/Chromium |
| 数据库 | MySQL 8.0（或 MariaDB 10.x） | 数据库名 `ljxz`，字符集 `utf8mb4` |
| 容器化 | Docker + Docker Compose | 一键部署 |

> **注意**：前端 `package.json` 中未列出 `element-plus` 和 `pinia`，实际在代码中 Element Plus 通过 CDN 引入，Pinia 未实际使用。

---

## 3. 项目目录结构

```
项目根目录
├── vue-cycling-app/           # Vue3 前端
│   ├── src/
│   │   ├── views/             # 页面组件（Home, Login, RoutePlanning, Equipment...）
│   │   ├── components/        # 可复用组件（图表组件、Navbar、Footer）
│   │   ├── router/index.js    # Vue Router 配置，含路由守卫
│   │   ├── services/api.js    # Axios 封装，统一调用双后端
│   │   ├── config/api.js      # API 端点与错误码配置
│   │   └── utils/auth.js      # JWT 认证工具
│   ├── vite.config.js         # Vite 配置，含开发代理规则
│   └── package.json           # 前端依赖
├── java-backend/              # Java 主后端
│   ├── src/main/java/com/ljxz/cycling/
│   │   ├── CyclingRouteApplication.java   # 启动类
│   │   ├── controller/        # REST 控制器（Route, Auth, User）
│   │   ├── service/           # 业务逻辑（AmapService, RouteService, AuthService）
│   │   ├── config/            # 安全配置、JWT 过滤器、全局异常处理
│   │   ├── entity/            # JPA 实体
│   │   ├── dto/               # 请求/响应 DTO
│   │   ├── repository/        # Spring Data JPA Repository
│   │   └── util/              # JWT 工具类
│   ├── src/main/resources/application.yml   # 主配置（数据库、JWT、高德API）
│   └── pom.xml                # Maven 配置
├── python-backend/            # Python 爬虫服务
│   ├── app.py                 # Flask 应用主入口（约 1643 行， monolithic）
│   ├── start.py               # 启动脚本（含依赖检查、数据库初始化、调度器启动）
│   ├── scheduler.py           # APScheduler 定时任务调度
│   ├── models/equipment.py    # SQLAlchemy 模型工厂（Category, Equipment, Price, Review）
│   ├── services/              # 业务服务（crawler, equipment, data_analysis, monitor, queue...）
│   ├── config/crawler_config.json   # 爬虫配置（平台、分类、关键词、反爬策略）
│   ├── database/equipment_tables.sql    # 装备相关表结构
│   ├── requirements.txt       # Python 依赖
│   └── .env.example           # 环境变量模板
├── database/
│   ├── complete_init.sql      # 完整数据库初始化脚本（含用户、路线、装备全量表）
│   └── test_data.sql          # 测试数据
├── launcher/
│   ├── launcher.py            # Tkinter GUI 启动器（MariaDB + Java + Python 一键启动）
│   └── launcher.spec          # PyInstaller 打包配置
├── docker-compose.yml         # Docker Compose（MySQL + Java + Python + Nginx 前端）
├── start_local.bat            # Windows 本地一键启动（要求已编译 JAR、.venv、node_modules）
├── start_docker.bat           # Windows Docker 一键启动
└── docs/                      # 项目文档（7 个章节，全中文）
```

---

## 4. 关键配置文件说明

### 4.1 前端代理规则（`vue-cycling-app/vite.config.js`）

开发模式下，Vite 开发服务器代理规则如下：
- `/api/equipment` → `http://localhost:5000`（Python 后端）
- `/api/crawler` → `http://localhost:5000`（Python 后端）
- `/api` → `http://localhost:8080`（Java 后端）

**重要**：生产环境（Docker）中，前端通过 Nginx 代理，`/api/` 统一转发到 `java-backend:8080/api/`。Python 后端 API 在生产环境中需直接通过 `http://localhost:5000/api` 访问，或在 Nginx 中额外配置 location。

### 4.2 Java 后端配置（`java-backend/src/main/resources/application.yml`）

- 服务端口：`8080`，上下文路径：`/api`
- 数据库：`jdbc:mysql://localhost:3306/ljxz`
- 高德地图 API Key：配置在 `amap.web-api-key` / `js-api-key` / `security-key`
- JWT 密钥：`ljxz-cycling-route-secret-key-2024`，有效期 24 小时，Refresh Token 7 天
- 免认证路径：`/auth/**`, `/health`, `/route/health`, `/public/**` 等
- MyBatis 配置当前被注释掉，项目实际使用 Spring Data JPA

### 4.3 Python 后端环境变量

从 `.env` 或环境变量读取：
- `DATABASE_URL` / `DB_HOST` / `DB_PORT` / `DB_USER` / `DB_PASSWORD` / `DB_NAME`
- `SECRET_KEY` — Flask session 密钥
- `VUE_DIST_DIR` — 若设置，Flask 会以 static_folder 模式 serve Vue 构建产物
- `CHROME_BINARY_PATH` / `CHROMEDRIVER_PATH` — Docker 中指向 `/usr/bin/chromium`

---

## 5. 构建与运行命令

### 5.1 前端（`vue-cycling-app/`）

```bash
npm install
npm run dev          # 开发模式，默认端口 5500（vite.config.js 中配置）
npm run build        # 生产构建，输出到 dist/
npm run preview      # 预览生产构建
```

### 5.2 Java 后端（`java-backend/`）

```bash
mvn clean install    # 编译并打包 JAR（target/cycling-route-backend-1.0.0.jar）
mvn spring-boot:run  # 直接运行（开发模式）
```

### 5.3 Python 后端（`python-backend/`）

```bash
# 创建虚拟环境（项目要求 .venv 目录）
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

pip install -r requirements.txt
python start.py        # 推荐：含依赖检查、数据库连接检查、调度器启动
# 或
python app.py          # 直接启动 Flask（不含调度器）
```

### 5.4 数据库初始化

```bash
mysql -u root -p -e "CREATE DATABASE ljxz CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p ljxz < database/complete_init.sql
```

### 5.5 Docker 一键部署（项目根目录）

```bash
# Windows
double-click start_docker.bat
# 或命令行
docker-compose -p cycling_system up -d --build
```

Docker Compose 启动 4 个服务：
- MySQL（端口映射 `3307:3306`）
- Java 后端（`8080:8080`）
- Python 后端（`5000:5000`）
- Vue 前端（Nginx，`80:80`）

### 5.6 Windows 本地一键启动（开发/测试）

```bash
# 前提：Java 后端已编译出 JAR、Python .venv 已创建、前端 node_modules 已安装
double-click start_local.bat
```

该脚本会自动：
1. 检测并启动 Java 后端（端口 8080）
2. 启动 Python 后端（端口 5000，含调度器）
3. 启动 Vue 前端（Vite，端口 5500/5510/5520 自动探测）
4. 前端退出时自动关闭两个后端

---

## 6. 代码组织与模块划分

### 6.1 前端（Vue 3）

- **路由**：`src/router/index.js` 使用 `createWebHistory`，部分页面（`feedback`, `vr`, `route-planning`）需要登录认证（`meta: { requiresAuth: true }`）。
- **API 调用**：`src/services/api.js` 封装了 `ApiService` 静态类，按领域分组（`user`, `routes`, `routePlanning`, `records`, `feedback`, `equipment`, `crawler`, `analysis`）。
- **认证**：JWT 存储在 `localStorage`（`token`, `accessToken`, `refreshToken`, `userInfo`），Axios 请求拦截器自动附加 `Authorization: Bearer <token>`。
- **图表组件**：`PriceHistoryChart.vue`, `BrandMarketShareChart.vue`, `PriceDistributionChart.vue`, `BrandRadarChart.vue` 均基于 Chart.js，调用 Python 后端 `/api/analysis/*` 接口。

### 6.2 Java 后端（Spring Boot）

- **包结构**：`com.ljxz.cycling`，按功能分层（controller / service / repository / entity / dto / config / util）。
- **入口类**：`CyclingRouteApplication`
- **核心服务**：
  - `RouteService` — 路径规划业务逻辑，调用 `AmapService` 对接高德 API
  - `AuthService` — 用户注册、登录、Token 刷新
  - `UserDetailsServiceImpl` — Spring Security 用户详情服务
- **安全配置**：`SecurityConfig` + `JwtAuthenticationFilter`，密码使用 BCrypt 加密。
- **全局异常**：`GlobalExceptionHandler` 统一处理参数校验失败、业务异常。

### 6.3 Python 后端（Flask）

- **单文件入口**：`app.py` 是一个约 1643 行的 monolithic 文件，包含所有路由定义。新增接口时通常在此文件追加路由函数。
- **模型工厂**：`models/equipment.py` 使用 `create_models(db)` 工厂函数动态创建 SQLAlchemy 模型类，避免循环导入。
- **服务层**：`services/` 目录包含多个模块：
  - `crawler_service.py` / `advanced_crawler_service.py` — 爬虫核心
  - `equipment_service.py` — 装备 CRUD 与搜索
  - `data_analysis_service.py` — 价格趋势、市场竞争、推荐算法
  - `crawler_config_service.py` — 爬虫配置管理（读写 `config/crawler_config.json`）
  - `crawler_monitor_service.py` — 爬虫监控与系统指标采集
  - `crawler_queue_service.py` — 爬虫任务队列管理
- **调度器**：`scheduler.py` 使用 APScheduler 执行定时爬虫、价格更新、数据清理任务。

---

## 7. 开发规范

### 7.1 代码风格

- **注释与文档**：优先使用中文，关键术语附英文对照。
- **前端**：遵循 Vue 3 官方风格指南，使用 Composition API（`setup` 语法）。
- **Java**：遵循 Spring Boot 最佳实践，使用 Lombok 简化 POJO，Controller 层使用 `@Slf4j` 日志。
- **Python**：遵循 PEP 8，使用 4 空格缩进。

### 7.2 提交规范

格式：`<type>(<scope>): <subject>`

| Type | 含义 |
|------|------|
| feat | 新功能 |
| fix | 修复 Bug |
| docs | 文档更新 |
| style | 代码格式 |
| refactor | 重构 |
| test | 测试 |
| chore | 构建/工具 |

示例：`feat(route): 添加骑行路径规划功能`

### 7.3 分支管理

- `main` — 主分支，生产环境代码
- `develop` — 开发分支，集成测试
- `feature/xxx` — 功能分支
- `bugfix/xxx` — Bug 修复分支
- `hotfix/xxx` — 热修复分支
- `release/xxx` — 发布分支

---

## 8. 测试策略

> **现状说明**：项目文档中列出了完整的测试策略矩阵，但实际代码中**单元测试和集成测试文件极少**（根目录下仅发现 `database/test_data.sql`）。如果需要添加测试，请按以下规范创建：

| 层级 | 前端 | Java 后端 | Python 后端 |
|------|------|-----------|-------------|
| 单元测试 | Vitest | JUnit 5 | pytest |
| 集成测试 | Cypress | Spring Boot Test | pytest + requests |
| E2E 测试 | Playwright | TestContainers | Selenium |

**健康检查端点**（用于快速验证服务状态）：
- Java：`GET http://localhost:8080/api/route/health`
- Python：`GET http://localhost:5000/api/health`

---

## 9. 安全注意事项

### 9.1 敏感信息

以下文件中**包含硬编码密钥**，生产部署前必须修改：
- `java-backend/src/main/resources/application.yml`：
  - `amap.web-api-key` / `js-api-key` / `security-key`（高德地图 API Key）
  - `jwt.secret`（JWT 签名密钥）
  - `spring.datasource.password`（数据库密码）
- `python-backend/.env`（若存在）：数据库密码、邮件密码
- `launcher/launcher.py`：`DB_PASS = "Cycling2024!"`

### 9.2 认证与授权

- 前端通过 `localStorage` 存储 JWT，存在 XSS 风险。当前代码在 `api.js` 响应拦截器中，遇到 401 会自动清除 Token 并跳转到登录页。
- Java 后端的 `SecurityConfig` 配置了 CORS 和 JWT 过滤器，`/auth/**` 和 `/health` 等路径无需认证。
- 密码使用 BCrypt 加密存储（`users.password_hash`）。

### 9.3 爬虫合规

- Python 后端爬虫配置（`config/crawler_config.json`）包含请求延迟、User-Agent 轮换、随机延迟等反检测策略。
- 爬虫默认爬取淘宝、京东等电商平台，请确保遵守相关平台的 `robots.txt` 和使用条款。

---

## 10. 部署方式总览

| 方式 | 适用场景 | 入口文件 | 说明 |
|------|----------|----------|------|
| Docker Compose | 推荐，生产/演示 | `start_docker.bat` / `docker-compose.yml` | 一键启动全部 4 个服务 |
| 本地开发 | 开发调试 | `start_local.bat` | 要求预编译 JAR、.venv、node_modules |
| 完全手动 | 细粒度控制 | — | 分别启动 MySQL、Java、Python、Vue |
| 打包发行 | 无 Docker 环境分发 | `launcher/launcher.py` + PyInstaller | 捆绑 MariaDB + JRE + Python EXE + Vue 静态文件 |

---

## 11. 常见问题与排查

1. **Java 后端启动失败**
   - 检查 `java-backend/target/cycling-route-backend-1.0.0.jar` 是否存在
   - 检查 `java_logs.txt`（`start_local.bat` 输出）
   - 确认 MySQL 服务已启动且 `ljxz` 数据库已创建

2. **Python 后端启动失败**
   - 检查 `.venv` 是否存在且依赖已安装
   - 检查 `python_logs.txt`
   - 确认数据库连接配置正确（`.env` 或环境变量）

3. **前端请求 404/502**
   - 开发模式：检查 Vite 代理配置（`vite.config.js`）
   - 生产模式（Docker）：检查 Nginx 配置是否正确代理 `/api/` 到 Java 后端
   - Python 后端 API（`/api/equipment`）在生产 Nginx 配置中**未单独代理**，可能需要额外配置

4. **数据库乱码**
   - 确保 MySQL/MariaDB 字符集为 `utf8mb4`
   - 确保连接 URL 包含 `useUnicode=true&characterEncoding=utf8`

---

## 12. 许可证与贡献

- **许可证**：双重许可模式
  - 非商业用途：GNU AGPL-3.0
  - 商业用途：须签署书面商业授权协议
- **贡献者许可协议（CLA）**：向本项目提交任何贡献即视为同意 CLA 条款，全部著作权无偿转让给项目方（河北经贸大学 灵境行者团队）。详见 `CONTRIBUTING.md`。
- **联系人**：陈冠衡，925342921@qq.com

---

*本文档基于项目实际代码生成。若项目结构或配置发生变化，请及时更新本文件。*
