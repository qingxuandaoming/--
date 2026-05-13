# 灵境行者数据库设置指南

> **更新时间**: 2025年1月  
> **版本**: v2.1.0  
> **适用于**: MySQL 8.0+  

本指南将帮助您设置灵境行者项目所需的MySQL数据库，包括Java后端和Python后端的数据库配置。项目采用统一的数据库设计，支持用户管理、骑行路线、装备信息等核心功能。

## 📋 前置要求

- **MySQL**: 8.0 或更高版本
- **数据库管理工具**: MySQL Workbench、phpMyAdmin 或命令行工具
- **权限**: 数据库创建和管理权限
- **字符集**: 支持UTF-8编码

## 🔧 数据库配置

### 默认连接配置

项目使用以下默认数据库连接配置：

```yaml
# Java后端配置 (application.yml)
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/ljxz?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver
```

```python
# Python后端配置
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'ljxz',
    'charset': 'utf8mb4'
}
```

### 修改数据库配置

#### Java后端配置
修改 `java-backend/src/main/resources/application.yml`：

```yaml
spring:
  datasource:
    url: jdbc:mysql://your-host:your-port/your-database?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: your-username
    password: your-password
```

#### Python后端配置
修改 `python-backend/config.py`：

```python
DATABASE_URL = 'mysql+pymysql://username:password@host:port/database'
```

#### 环境变量配置（推荐）
为了安全性，建议使用环境变量：

```bash
# 设置环境变量
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=your-password
export DB_NAME=ljxz
```

## 🗄️ 数据库初始化

### 1. 创建数据库和表结构

执行以下步骤初始化数据库：

```bash
# 1. 登录MySQL
mysql -u root -p

# 2. 执行初始化脚本
source /path/to/your/project/database/init.sql

# 或者直接导入
mysql -u root -p < database/init.sql
```

### 2. 验证数据库创建

```sql
-- 查看数据库
SHOW DATABASES;

-- 使用数据库
USE ljxz;

-- 查看表结构
SHOW TABLES;

-- 查看示例数据
SELECT * FROM cycling_routes;
```

## 📊 数据库表结构

项目包含以下主要数据表：

### 1. users（用户表）
- 存储用户基本信息
- 包含用户名、邮箱、密码等字段

### 2. cycling_routes（骑行路线表）
- 存储骑行路线信息
- 包含路线名称、描述、难度等级等

### 3. cycling_records（骑行记录表）
- 存储用户的骑行记录
- 包含骑行时间、距离、速度等数据

### 4. feedback（反馈表）
- 存储用户反馈信息
- 包含反馈主题、内容、状态等

### 5. route_favorites（路线收藏表）
- 存储用户收藏的路线

### 6. route_ratings（路线评分表）
- 存储用户对路线的评分和评论

## 🔌 在项目中使用数据库

### 1. 导入数据库工具类

```javascript
import Database from '@/utils/database.js';
```

### 2. 基本操作示例

```javascript
// 查询数据
const routes = await Database.query('SELECT * FROM cycling_routes WHERE difficulty_level = ?', ['easy']);

// 插入数据
const newUser = {
  username: 'testuser',
  email: 'test@example.com',
  password_hash: 'hashed_password'
};
const result = await Database.insert('users', newUser);

// 更新数据
const updateData = { full_name: 'Test User' };
await Database.update('users', updateData, 'id = ?', [userId]);

// 删除数据
await Database.delete('users', 'id = ?', [userId]);
```

### 3. 使用API服务

```javascript
import ApiService from '@/services/api.js';

// 获取所有路线
const routes = await ApiService.routes.getAll();

// 用户登录
const loginResult = await ApiService.user.login({
  username: 'testuser',
  password: 'password'
});
```

## 🧪 测试数据库连接

### Java后端测试

```bash
# 启动Java应用后访问健康检查端点
curl http://localhost:8080/actuator/health

# 测试数据库连接
curl http://localhost:8080/api/test/db
```

### Python后端测试

```bash
# 测试Python服务健康状态
curl http://localhost:5000/api/health

# 测试数据库连接
curl http://localhost:5000/api/test/db
```

### 前端测试

```javascript
// 在浏览器控制台中测试API连接
fetch('/api/test/db')
  .then(response => response.json())
  .then(data => console.log('数据库连接状态:', data));
```

## 🔍 故障排除

### 1. 连接失败问题

**症状**: `Connection refused` 或 `Access denied`

**解决方案**:
```bash
# 检查MySQL服务状态
sudo systemctl status mysql
# 或 Windows 下
net start mysql80

# 检查端口是否开放
netstat -an | grep 3306

# 测试连接
mysql -h localhost -u root -p
```

### 2. 字符编码问题

**症状**: 中文字符显示为乱码

**解决方案**:
```sql
-- 检查数据库字符集
SHOW VARIABLES LIKE 'character_set%';

-- 修改数据库字符集
ALTER DATABASE ljxz CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 修改表字符集
ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 权限问题

**症状**: `Access denied for user`

**解决方案**:
```sql
-- 创建用户并授权
CREATE USER 'ljxz_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON ljxz.* TO 'ljxz_user'@'localhost';
FLUSH PRIVILEGES;

-- 检查用户权限
SHOW GRANTS FOR 'ljxz_user'@'localhost';
```

### 4. 时区问题

**症状**: 时间数据不正确

**解决方案**:
```sql
-- 设置时区
SET GLOBAL time_zone = '+8:00';
SET time_zone = '+8:00';

-- 在连接URL中指定时区
jdbc:mysql://localhost:3306/ljxz?serverTimezone=Asia/Shanghai
```

## 🚀 性能优化

### 1. 索引优化

```sql
-- 为常用查询字段创建索引
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_route_difficulty ON cycling_routes(difficulty_level);
CREATE INDEX idx_record_date ON cycling_records(created_at);
```

### 2. 连接池配置

```yaml
# Java后端连接池配置
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
```

### 3. 查询优化

```sql
-- 使用EXPLAIN分析查询性能
EXPLAIN SELECT * FROM cycling_routes WHERE difficulty_level = 'easy';

-- 避免SELECT *，只查询需要的字段
SELECT id, name, difficulty_level FROM cycling_routes WHERE difficulty_level = 'easy';
```

## 🔒 安全最佳实践

### 1. 密码安全
- 使用强密码
- 定期更换数据库密码
- 使用环境变量存储敏感信息

### 2. 网络安全
```sql
-- 限制远程访问
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'strong_password';
-- 而不是 'app_user'@'%'
```

### 3. 备份策略
```bash
# 定期备份数据库
mysqldump -u root -p ljxz > backup_$(date +%Y%m%d_%H%M%S).sql

# 自动备份脚本
#!/bin/bash
BACKUP_DIR="/path/to/backup"
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u root -p ljxz > $BACKUP_DIR/ljxz_backup_$DATE.sql
```

## 📊 监控和维护

### 1. 性能监控
```sql
-- 查看慢查询
SHOW VARIABLES LIKE 'slow_query_log';
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- 查看连接状态
SHOW PROCESSLIST;
SHOW STATUS LIKE 'Threads_connected';
```

### 2. 存储空间监控
```sql
-- 查看数据库大小
SELECT 
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'ljxz'
GROUP BY table_schema;
```

## 📝 注意事项

1. **生产环境配置**:
   - 使用专用数据库用户，避免使用root
   - 启用SSL连接
   - 配置防火墙规则
   - 定期备份数据

2. **开发环境配置**:
   - 可以使用Docker快速搭建
   - 使用测试数据，避免影响生产数据
   - 启用详细日志便于调试

3. **数据迁移**:
   - 在更新数据库结构前先备份
   - 使用版本控制管理数据库变更
   - 测试迁移脚本

## 🔗 相关文档

### 项目文档
- [项目总览](../README.md) - 项目整体介绍和架构
- [前端应用文档](./README.md) - Vue3前端应用详细文档
- [Java后端文档](../java-backend/README.md) - Spring Boot后端服务文档
- [Python后端文档](../python-backend/README.md) - Flask爬虫服务文档

### 数据库文档
- [数据库设计文档](../docs/DATABASE.md) - 完整的数据库设计和架构文档
- [API接口文档](./API_ENDPOINTS.md) - 数据库相关API接口说明
- [完整初始化脚本](../database/complete_init.sql) - 数据库建表脚本
- [测试数据脚本](../database/test_data.sql) - 测试数据插入脚本

### 技术文档
- [架构设计文档](../docs/ARCHITECTURE.md) - 系统架构设计
- [开发指南](../docs/DEVELOPMENT.md) - 开发环境搭建和规范
- [部署文档](../docs/DEPLOYMENT.md) - 生产环境部署指南
- [安全文档](../docs/SECURITY.md) - 安全策略和最佳实践

### 外部资源
- [MySQL官方文档](https://dev.mysql.com/doc/) - MySQL数据库官方文档
- [Spring Boot数据库配置](https://docs.spring.io/spring-boot/docs/current/reference/html/data.html) - Spring Boot数据库配置指南
- [Flask-SQLAlchemy文档](https://flask-sqlalchemy.palletsprojects.com/) - Python Flask数据库ORM

---

## 📝 更新日志

### v2.1.0 (2025年1月)
- 更新数据库配置示例
- 添加装备相关表的配置说明
- 完善监控和维护章节
- 更新相关文档链接

### v2.0.0 (2024年12月)
- 重构数据库设置流程
- 添加Docker配置支持
- 完善环境变量配置
- 优化数据库初始化脚本

---

*最后更新时间：2025年1月*