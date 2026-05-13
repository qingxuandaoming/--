# 电商数据API接口使用指南

## 概述

为了解决大型电商平台反爬机制强的问题，我们集成了第三方API接口来获取商品数据。系统支持多种数据获取方式，包括API接口、Selenium爬虫等。

## 支持的API提供商

### 1. 万邦开放平台 (Onebound)
- **官网**: https://www.onebound.cn/
- **支持平台**: 淘宝、天猫、京东、1688等
- **数据类型**: 商品搜索、商品详情、店铺信息、评价数据
- **费用**: 按调用次数计费，约0.01-0.05元/次

### 2. 聚合数据 (Juhe)
- **官网**: https://www.juhe.cn/
- **支持平台**: 多个电商平台
- **数据类型**: 商品信息、价格监控
- **费用**: 按调用次数计费

## API配置步骤

### 1. 注册API账号

#### 万邦开放平台注册步骤：
1. 访问 https://www.onebound.cn/
2. 注册账号并完成实名认证
3. 创建应用，获取 `app_key` 和 `app_secret`
4. 充值账户余额

### 2. 配置API密钥

使用以下API接口配置密钥：

```bash
# 配置万邦API
curl -X POST http://localhost:5000/api/crawler/api-config \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "onebound",
    "app_key": "your_app_key",
    "app_secret": "your_app_secret"
  }'
```

### 3. 查看API配置状态

```bash
# 获取API配置状态
curl http://localhost:5000/api/crawler/api-config
```

响应示例：
```json
{
  "success": true,
  "data": {
    "onebound": {
      "enabled": true,
      "configured": true
    },
    "juhe": {
      "enabled": false,
      "configured": false
    }
  }
}
```

## 爬取方式配置

### 查看当前爬取方式

```bash
curl http://localhost:5000/api/crawler/crawl-method
```

### 设置爬取方式

```bash
# 启用API方式
curl -X PUT http://localhost:5000/api/crawler/crawl-method \
  -H "Content-Type: application/json" \
  -d '{
    "method": "api",
    "enabled": true
  }'

# 禁用Selenium方式（可选）
curl -X PUT http://localhost:5000/api/crawler/crawl-method \
  -H "Content-Type: application/json" \
  -d '{
    "method": "selenium",
    "enabled": false
  }'
```

## 启动爬虫任务

配置完成后，可以正常启动爬虫任务：

```bash
# 启动爬虫任务
curl -X POST http://localhost:5000/api/crawler/start \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "all",
    "category": "bike"
  }'
```

系统会自动按照以下优先级选择数据获取方式：
1. **API接口**（优先，稳定可靠）
2. **Selenium爬虫**（备用，应对API失败）

## 费用说明

### 万邦开放平台费用参考
- 商品搜索API: 0.01元/次
- 商品详情API: 0.02元/次
- 店铺信息API: 0.01元/次
- 评价数据API: 0.03元/次

### 成本优化建议
1. **合理设置爬取频率**：避免过于频繁的API调用
2. **使用缓存机制**：相同查询在短时间内使用缓存结果
3. **精确关键词**：使用更精确的关键词减少无效调用
4. **分批处理**：大量数据分批次处理，避免超时

## 优势对比

| 方式 | 稳定性 | 速度 | 成本 | 数据质量 | 反爬风险 |
|------|--------|------|------|----------|----------|
| API接口 | 高 | 快 | 低 | 高 | 无 |
| Selenium | 中 | 慢 | 无 | 中 | 高 |
| Requests | 低 | 快 | 无 | 低 | 极高 |

## 故障排除

### 常见问题

1. **API调用失败**
   - 检查API密钥是否正确
   - 确认账户余额充足
   - 检查网络连接

2. **数据获取不完整**
   - 调整关键词策略
   - 增加API调用间隔
   - 检查API返回的错误信息

3. **成本过高**
   - 优化关键词列表
   - 启用缓存机制
   - 调整爬取频率

### 日志查看

系统会记录详细的API调用日志，可以通过以下方式查看：

```bash
# 查看爬虫任务状态
curl http://localhost:5000/api/crawler/status/{task_id}
```

## 技术支持

如果在使用过程中遇到问题，可以：

1. 查看系统日志文件
2. 检查API提供商的官方文档
3. 联系API提供商技术支持
4. 提交GitHub Issue

## 更新日志

- **v1.0.0**: 初始版本，支持万邦开放平台API
- **v1.1.0**: 添加聚合数据API支持
- **v1.2.0**: 优化错误处理和重试机制