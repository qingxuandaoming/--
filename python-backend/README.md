# 灵境行者 - Python爬虫服务

## 项目简介

灵境行者Python爬虫服务是基于Flask开发的专业爬虫API服务，专注于骑行装备数据的采集、处理和分析。作为项目生态的重要组成部分，与Java主服务协同工作，为前端Vue应用提供丰富的骑行装备信息和智能推荐功能。

### 数据库集成
- **共享数据库**: MySQL 8.0 或 SQLite，数据库名：`ljxz`（与Java后端共享）
- **ORM框架**: SQLAlchemy
- **连接池**: SQLAlchemy连接池管理
- **主要数据表**: `equipment`, `equipment_categories`, `equipment_price_history`, `equipment_reviews`
- **数据同步**: 与Java后端实时数据同步

## 🚀 功能特性

### 核心爬虫功能
- 🕷️ **多平台数据采集**：支持淘宝、京东等主流电商平台的骑行装备信息爬取
- 🔄 **智能任务调度**：异步爬虫任务管理，支持批量和定时爬取
- 🛡️ **反反爬策略**：集成多种反爬虫对抗技术，确保数据采集稳定性
- 📊 **数据清洗**：自动清洗和标准化爬取的装备数据
- 💾 **数据存储**：结构化存储装备信息，支持MySQL和SQLite数据库

### 搜索与推荐
- 🔍 **多维度搜索**：支持关键词、分类、价格区间、平台等多条件搜索
- 💰 **价格比较**：跨平台价格对比分析
- 🎯 **智能分类**：自动识别和分类骑行装备类型
- 📈 **数据统计**：装备价格趋势、销量分析等统计功能

### 数据分析与可视化
- 📊 **价格趋势分析**：多平台历史价格变化趋势
- 🏆 **品牌市场份额**：各品牌市场占有率分析
- 💹 **价格分布统计**：不同价格区间产品分布
- 🔍 **市场竞争分析**：品牌竞争力和市场概况

### API服务
- 📱 **RESTful接口**：标准化API设计，易于前端集成
- 🔗 **服务协作**：与Java后端无缝集成，提供完整的数据服务
- 🚀 **高性能**：异步处理和缓存机制，保证服务响应速度
- 📋 **任务管理**：爬虫任务状态监控和管理接口

### 高级功能
- ⚙️ **爬虫配置管理**：动态配置爬虫平台、分类、关键词
- 📈 **实时监控**：爬虫性能监控、系统指标监控
- 🔄 **队列管理**：任务队列的创建、暂停、恢复、取消、重试
- ✅ **数据验证**：装备数据质量验证和批量验证

### 装备分类
- **自行车**: 山地车、公路车、折叠车、电动车、城市车
- **骑行服装**: 骑行上衣、骑行裤、手套、鞋子、袜子
- **安全防护**: 头盔、护膝护肘、反光装备
- **骑行配件**: 车灯、码表、水壶架、车锁、车包
- **自行车零件**: 轮胎、刹车、变速器等
- **维修工具**: 打气筒、工具包等

## 📋 系统要求

- Python 3.8+
- MySQL 5.7+ （或 SQLite）
- Chrome浏览器（用于Selenium爬虫）
- Redis（可选，用于缓存）

## 🛠️ 安装指南

### 1. 进入项目目录
```bash
cd python-backend
```

### 2. 创建虚拟环境
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，配置数据库连接等信息
```

### 5. 初始化数据库
```bash
# 确保MySQL服务已启动
# 执行数据库初始化脚本
mysql -u root -p < ../vue-cycling-app/database/init.sql
```

### 6. 安装Chrome驱动
```bash
# 使用webdriver-manager自动管理ChromeDriver
pip install webdriver-manager
```

## 🚀 运行服务

### 启动主服务
```bash
python app.py
```
服务将在 `http://localhost:5000` 启动

### 启动定时任务调度器
```bash
python scheduler.py
```

## 📡 API接口

### 健康检查
```http
GET /api/health
```

### 装备分类
```http
GET /api/equipment/categories
```

### 搜索装备
```http
GET /api/equipment/search?keyword=山地车&category_id=1&min_price=100&max_price=5000&platform=taobao&page=1&per_page=20
```

### 获取装备列表
```http
GET /api/equipment?category_id=1&sort_by=rating&page=1&per_page=20
```

### 获取装备详情
```http
GET /api/equipment/1
```

### 获取装备价格历史
```http
GET /api/equipment/1/prices?days=30
```

### 获取装备推荐
```http
GET /api/equipment/1/recommendations
```

### 手动触发爬虫
```http
POST /api/equipment/crawl
Content-Type: application/json

{
  "platform": "taobao",
  "category": "helmet"
}
```

### 获取爬虫任务状态
```http
GET /api/equipment/crawl/status/<task_id>
```

### 高级爬虫
```http
POST /api/advanced-crawler/start
Content-Type: application/json

{
  "platforms": ["taobao", "jd"],
  "categories": ["bike", "helmet"],
  "keywords": ["山地车", "公路车"],
  "max_items_per_keyword": 50
}
```

```http
GET /api/advanced-crawler/status/<task_id>
GET /api/advanced-crawler/tasks
```

### 数据分析
```http
GET /api/analysis/trends?days=30
GET /api/analysis/competition?category=bike
GET /api/analysis/price-alerts?threshold=10.0
GET /api/analysis/recommendations?category=bike&min_budget=1000&max_budget=5000&limit=10
POST /api/analysis/clear-cache
```

### 图表数据
```http
GET /api/analysis/price-history/<equipment_id>?days=30
GET /api/analysis/brand-market-share?category=bike
GET /api/analysis/price-distribution
```

### 爬虫配置管理
```http
GET /api/config/crawler?key=xxx
PUT /api/config/crawler
GET /api/config/crawler/summary
GET /api/config/crawler/platforms
GET /api/config/crawler/categories
GET /api/config/crawler/keywords/<category>
POST /api/config/crawler/keywords/<category>
DELETE /api/config/crawler/keywords/<category>
PUT /api/config/crawler/platform/<platform>/status
PUT /api/config/crawler/category/<category>/status
POST /api/config/crawler/reset
GET /api/config/crawler/export
```

### 爬虫监控
```http
POST /api/monitor/start
POST /api/monitor/stop
GET /api/monitor/stats/current
GET /api/monitor/stats/history?limit=100
GET /api/monitor/metrics/current
GET /api/monitor/metrics/history?limit=100
GET /api/monitor/errors
GET /api/monitor/performance
GET /api/monitor/database
GET /api/monitor/report
POST /api/monitor/clear-history
```

### 爬虫队列管理
```http
POST /api/queue/start
POST /api/queue/stop
POST /api/queue/tasks
GET /api/queue/tasks?status=PENDING&limit=100
GET /api/queue/tasks/<task_id>
POST /api/queue/tasks/<task_id>/cancel
POST /api/queue/tasks/<task_id>/pause
POST /api/queue/tasks/<task_id>/resume
POST /api/queue/tasks/<task_id>/retry
GET /api/queue/status
POST /api/queue/cleanup
```

### 数据验证
```http
POST /api/validation/validate
POST /api/validation/batch
GET /api/validation/summary
```

## 🗄️ 数据库设计

### 主要数据表
- `equipment_categories`: 装备分类表
- `equipment`: 装备基本信息表
- `equipment_prices`: 装备价格历史表
- `equipment_reviews`: 装备评价表

## 🕷️ 爬虫说明

### 支持平台
- **淘宝**: 使用Selenium模拟浏览器爬取
- **京东**: 使用Selenium模拟浏览器爬取

### 爬取策略
- 支持手动触发爬虫任务
- 实现反爬虫机制：随机User-Agent、请求延迟等
- 高级爬虫支持多平台、多关键词并发爬取

### 数据字段
- 商品名称、品牌、型号
- 价格、原价、折扣信息
- 商品图片、详情链接
- 卖家信息、销量数据
- 用户评价、评分统计

## 🔧 配置说明

### 环境变量
```env
# 数据库配置
DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/ljxz
# 或 SQLite: sqlite:///app.db

# Flask配置
SECRET_KEY=your-secret-key
DEBUG=True
HOST=0.0.0.0
PORT=5000

# 爬虫配置
CRAWL_DELAY=2
CRAWL_TIMEOUT=30
MAX_RETRY=3

# Vue打包目录（可选，用于静态文件服务）
VUE_DIST_DIR=../vue-cycling-app/dist
```

## 📊 监控和日志

### 日志配置
- 使用loguru进行日志管理
- 日志文件保存在 `logs/` 目录
- 支持不同级别的日志输出

### 性能监控
- 爬虫任务执行状态监控
- 数据库查询性能监控
- API响应时间统计
- 系统资源使用率监控（CPU、内存、磁盘）

## 🚨 注意事项

### 爬虫使用
1. **遵守robots.txt**: 尊重网站的爬虫协议
2. **合理频率**: 避免过于频繁的请求
3. **数据使用**: 仅用于学习和研究目的
4. **法律合规**: 确保符合相关法律法规

### 性能优化
1. **数据库索引**: 已为常用查询字段创建索引
2. **缓存策略**: 可配置Redis缓存热门数据
3. **异步处理**: 爬虫任务采用异步执行
4. **资源限制**: 控制并发爬虫数量

## 🔄 部署建议

### 生产环境
```bash
# 使用gunicorn部署
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 使用supervisor管理进程
# 配置nginx反向代理
```

### Docker部署
项目已提供Dockerfile，可直接构建镜像：
```bash
docker build -t ljxz-python-backend .
docker run -d -p 5000:5000 ljxz-python-backend
```

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目仅用于学习和研究目的。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 项目Issues

---

**注意**: 本项目中的爬虫功能仅用于技术学习和研究，请确保在使用时遵守相关网站的服务条款和法律法规。

*最后更新：2025年5月*
