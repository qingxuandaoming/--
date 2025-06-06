# 数据库设置指南

本项目使用MySQL作为数据库，以下是完整的设置和使用指南。

## 📋 前提条件

1. 确保已安装MySQL服务器（版本5.7或更高）
2. MySQL服务正在运行
3. 具有数据库创建权限的用户账户

## 🔧 数据库配置

### 1. 数据库连接信息

项目默认配置如下（可在 `src/config/database.js` 中修改）：

```javascript
{
  host: 'localhost',
  user: 'root',
  password: '123456',
  port: 3306,
  database: 'ljxz'
}
```

### 2. 修改数据库配置

如需修改数据库连接信息，请编辑 `src/config/database.js` 文件：

```javascript
const dbConfig = {
  host: 'your_host',        // 数据库主机地址
  user: 'your_username',    // 数据库用户名
  password: 'your_password', // 数据库密码
  port: 3306,               // 数据库端口
  database: 'your_database_name' // 数据库名称
};
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

项目提供了数据库连接测试工具：

```javascript
import { testDatabaseConnection, testDatabaseOperations } from '@/utils/dbTest.js';

// 测试连接
const isConnected = await testDatabaseConnection();

// 测试操作
const operationsWork = await testDatabaseOperations();
```

在开发模式下，测试会自动运行并在控制台显示结果。

## ⚠️ 注意事项

1. **安全性**：
   - 生产环境中请使用强密码
   - 不要在代码中硬编码敏感信息
   - 考虑使用环境变量存储数据库配置

2. **性能优化**：
   - 项目使用连接池管理数据库连接
   - 适当使用索引提高查询性能
   - 定期清理不必要的数据

3. **备份**：
   - 定期备份数据库
   - 在重要操作前创建数据快照

## 🔧 故障排除

### 常见问题

1. **连接被拒绝**：
   - 检查MySQL服务是否运行
   - 验证连接参数是否正确
   - 确认防火墙设置

2. **认证失败**：
   - 检查用户名和密码
   - 确认用户具有相应权限

3. **数据库不存在**：
   - 运行初始化脚本创建数据库
   - 检查数据库名称是否正确

### 调试技巧

- 查看浏览器控制台的错误信息
- 检查MySQL错误日志
- 使用数据库连接测试工具验证配置

## 📚 相关文档

- [MySQL官方文档](https://dev.mysql.com/doc/)
- [mysql2 NPM包文档](https://www.npmjs.com/package/mysql2)
- [Vue.js官方文档](https://vuejs.org/)