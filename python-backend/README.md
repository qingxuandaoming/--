# 灵境行者 - Python后端服务

这是灵境行者骑行应用的Python后端服务，主要负责骑行装备的爬取、搜索和推荐功能。

## 🚀 功能特性

### 核心功能
- **装备爬虫**: 支持淘宝、京东等平台的骑行装备数据爬取
- **智能搜索**: 基于关键词、分类、价格等多维度搜索
- **价格监控**: 实时监控装备价格变化，提供历史价格趋势
- **商品推荐**: 基于分类和品牌的智能推荐算法
- **价格提醒**: 用户可设置目标价格，达到时自动提醒

### 装备分类
- **自行车**: 山地车、公路车、折叠车、电动车、城市车
- **骑行服装**: 骑行上衣、骑行裤、手套、鞋子、袜子
- **安全防护**: 头盔、护膝护肘、反光装备
- **骑行配件**: 车灯、码表、水壶架、车锁、车包
- **自行车零件**: 轮胎、刹车、变速器等
- **维修工具**: 打气筒、工具包等

## 📋 系统要求

- Python 3.8+
- MySQL 5.7+
- Chrome浏览器（用于Selenium爬虫）
- Redis（可选，用于缓存）

## 🛠️ 安装指南

### 1. 克隆项目
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
mysql -u root -p < database/equipment_tables.sql
```

### 6. 安装Chrome驱动
```bash
# 下载ChromeDriver并添加到PATH
# 或者使用webdriver-manager自动管理
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

### 获取装备价格历史
```http
GET /api/equipment/{equipment_id}/prices?days=30
```

### 获取装备推荐
```http
GET /api/equipment/{equipment_id}/recommendations
```

### 手动触发爬虫
```http
POST /api/equipment/crawl
Content-Type: application/json

{
  "platform": "taobao",  // taobao, jd, all
  "category": "bike"     // bike, helmet, clothing, accessories, parts, all
}
```

### 获取爬虫任务状态
```http
GET /api/equipment/crawl/status/{task_id}
```

## 🗄️ 数据库设计

### 主要数据表
- `equipment_categories`: 装备分类表
- `equipment`: 装备基本信息表
- `equipment_prices`: 装备价格历史表
- `equipment_reviews`: 装备评价表
- `user_equipment_favorites`: 用户收藏表
- `price_alerts`: 价格提醒表

## 🕷️ 爬虫说明

### 支持平台
- **淘宝**: 使用Selenium模拟浏览器爬取
- **京东**: 使用Selenium模拟浏览器爬取

### 爬取策略
- 每日凌晨2点执行全量爬虫
- 每4小时更新热门商品价格
- 支持手动触发爬虫任务
- 实现反爬虫机制：随机User-Agent、请求延迟等

### 数据字段
- 商品名称、品牌、型号
- 价格、原价、折扣信息
- 商品图片、详情链接
- 卖家信息、销量数据
- 用户评价、评分统计

## ⏰ 定时任务

- **每日全量爬虫**: 每天凌晨2点
- **热门商品价格更新**: 每4小时
- **清理过期任务**: 每小时
- **更新装备评分**: 每天凌晨3点
- **检查价格提醒**: 每30分钟

## 🔧 配置说明

### 环境变量
```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=123456
DB_NAME=ljxz

# Flask配置
SECRET_KEY=your-secret-key
DEBUG=True
HOST=0.0.0.0
PORT=5000

# 爬虫配置
CRAWL_DELAY=2
CRAWL_TIMEOUT=30
MAX_RETRY=3
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
```dockerfile
# 可以创建Dockerfile进行容器化部署
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
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
- 邮箱: [your-email@example.com]

---

**注意**: 本项目中的爬虫功能仅用于技术学习和研究，请确保在使用时遵守相关网站的服务条款和法律法规。