# 增强爬虫系统功能说明

## 概述

本项目在原有爬虫功能基础上，新增了多个高级服务模块，提供更完善的数据处理、智能推荐和价格监控功能。

## 🆕 新增功能

### 1. 数据验证服务 (DataValidationService)

**功能特点:**
- 装备数据质量验证
- 价格合理性检查
- 重复数据检测
- 数据清洗和标准化
- 质量评分系统

**主要方法:**
- `validate_equipment_data()` - 验证单个装备数据
- `validate_batch_equipment_data()` - 批量验证装备数据
- `get_validation_summary()` - 获取验证统计摘要
- `clear_duplicate_cache()` - 清理重复数据缓存

### 2. 智能推荐服务 (RecommendationService)

**功能特点:**
- 基于内容的相似度推荐
- 价格区间智能匹配
- 热门装备推荐
- 分类推荐
- 个性化推荐算法

**主要方法:**
- `get_equipment_recommendations()` - 根据装备ID获取推荐
- `get_category_recommendations()` - 获取分类推荐
- `get_price_range_recommendations()` - 价格区间推荐
- `get_trending_recommendations()` - 热门推荐
- `get_similar_equipment()` - 相似装备推荐

### 3. 价格预警服务 (PriceAlertService)

**功能特点:**
- 多种预警类型（降价、涨价、目标价格、百分比变化）
- 邮件和Webhook通知
- 预警历史记录
- 用户个性化预警
- 自动监控线程

**主要方法:**
- `create_alert()` - 创建价格预警
- `update_alert()` - 更新预警规则
- `delete_alert()` - 删除预警
- `start_monitoring()` - 启动价格监控
- `stop_monitoring()` - 停止价格监控

## 📋 API端点

### 数据验证API

```http
# 验证单个装备数据
POST /api/validation/validate
Content-Type: application/json
{
  "equipment_data": {
    "name": "山地自行车 Giant ATX 830",
    "price": 2999.0,
    "platform": "taobao",
    "link": "https://item.taobao.com/item.htm?id=123456789",
    "category": "bike"
  }
}

# 批量验证装备数据
POST /api/validation/batch
Content-Type: application/json
{
  "equipment_list": [装备数据数组]
}

# 获取验证摘要
GET /api/validation/summary
```

### 推荐服务API

```http
# 根据装备ID获取推荐
GET /api/recommendations/equipment/{equipment_id}?limit=10

# 获取分类推荐
GET /api/recommendations/category/{category}?limit=10

# 价格区间推荐
GET /api/recommendations/price-range?min_price=1000&max_price=5000&category=bike&limit=10

# 热门推荐
GET /api/recommendations/trending?days=7&limit=10

# 推荐统计
GET /api/recommendations/stats
```

### 价格预警API

```http
# 创建价格预警
POST /api/alerts
Content-Type: application/json
{
  "equipment_id": 1,
  "alert_type": "price_drop",
  "threshold_value": 10.0,
  "user_id": "user123",
  "email": "user@example.com"
}

# 获取价格预警详情
GET /api/alerts/{alert_id}

# 更新价格预警
PUT /api/alerts/{alert_id}
Content-Type: application/json
{
  "threshold_value": 15.0,
  "is_active": true
}

# 删除价格预警
DELETE /api/alerts/{alert_id}

# 获取用户预警
GET /api/alerts/user/{user_id}

# 获取预警历史
GET /api/alerts/history?user_id=user123&days=30

# 获取预警统计
GET /api/alerts/stats

# 启动/停止价格监控
POST /api/alerts/start-monitoring
POST /api/alerts/stop-monitoring
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 确保Python版本 >= 3.8
python --version

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境

复制 `.env.example` 到 `.env` 并配置相关参数：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/crawler_db

# Flask配置
FLASK_ENV=development
DEBUG=True
HOST=0.0.0.0
PORT=5000

# 邮件配置（用于价格预警）
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### 3. 自动部署

运行自动部署脚本：

```bash
python setup_enhanced_crawler.py
```

### 4. 手动启动

```bash
# 初始化数据库
python init_data.py

# 启动应用
python app.py
```

### 5. 测试功能

```bash
# 运行API测试
python test_new_apis.py
```

## 📊 数据验证配置

数据验证服务支持以下配置：

```python
# 价格范围配置
PRICE_RANGES = {
    'bike': (100, 50000),
    'helmet': (50, 2000),
    'clothing': (20, 1000),
    'accessories': (10, 500)
}

# 标题长度限制
TITLE_MIN_LENGTH = 5
TITLE_MAX_LENGTH = 200

# 必需字段
REQUIRED_FIELDS = ['name', 'price', 'platform', 'category']
```

## 🎯 推荐算法

推荐服务使用多种算法：

1. **内容相似度**: 基于TF-IDF和余弦相似度
2. **价格相似度**: 基于价格区间匹配
3. **热门度**: 基于销量和评价数据
4. **分类匹配**: 基于装备分类和关键词

## ⚠️ 价格预警类型

支持以下预警类型：

- `price_drop`: 价格下降预警
- `price_rise`: 价格上涨预警
- `target_price`: 目标价格预警
- `percentage_change`: 百分比变化预警

## 📈 监控和统计

系统提供详细的监控和统计功能：

- 数据验证质量统计
- 推荐系统性能指标
- 价格预警触发统计
- 用户行为分析

## 🔧 配置说明

### 邮件通知配置

```python
# 在.env文件中配置
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### Webhook通知配置

```python
# 在创建预警时指定webhook_url
{
  "equipment_id": 1,
  "alert_type": "price_drop",
  "threshold_value": 10.0,
  "webhook_url": "https://your-webhook-url.com/notify"
}
```

## 🐛 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库配置
   - 确保数据库服务运行
   - 验证用户权限

2. **邮件发送失败**
   - 检查SMTP配置
   - 验证邮箱密码（使用应用专用密码）
   - 检查防火墙设置

3. **推荐结果为空**
   - 确保数据库中有足够的装备数据
   - 检查分类和价格范围参数

4. **价格监控不工作**
   - 检查监控线程是否启动
   - 验证预警规则配置
   - 查看日志文件

### 日志查看

```bash
# 查看应用日志
tail -f logs/crawler.log

# 查看错误日志
grep ERROR logs/crawler.log
```

## 📝 开发说明

### 扩展新功能

1. **添加新的验证规则**
   - 在 `DataValidationService` 中添加验证方法
   - 更新验证配置

2. **扩展推荐算法**
   - 在 `RecommendationService` 中实现新算法
   - 添加相应的API端点

3. **增加预警类型**
   - 在 `PriceAlertService` 中定义新类型
   - 实现相应的触发逻辑

### 性能优化

- 使用Redis缓存提高响应速度
- 数据库索引优化
- 异步处理大量数据
- 分页查询减少内存使用

## 📞 技术支持

如有问题，请查看：

1. 日志文件：`logs/crawler.log`
2. API测试脚本：`test_new_apis.py`
3. 部署脚本：`setup_enhanced_crawler.py`

---

**版本**: 2.0.0  
**更新日期**: 2024年  
**作者**: 灵境行者开发团队