# 数据库变更日志

> **项目**: 灵境行者 (ljxz)  
> **数据库**: MySQL 8.0+  
> **字符集**: utf8mb4  

本文档记录了灵境行者项目数据库结构的所有变更历史，包括表结构修改、索引优化、数据迁移等。

## 📋 版本历史

### v2.1.0 (2025年1月)

#### 🆕 新增功能
- 完善装备价格历史追踪功能
- 添加用户装备收藏系统
- 增强价格提醒功能
- 优化全文搜索索引

#### 🔧 表结构优化
- `equipment` 表：添加更多规格字段
- `equipment_price_history` 表：优化价格记录结构
- `user_equipment_favorites` 表：用户收藏功能
- `price_alerts` 表：价格提醒功能

#### 📊 索引优化
- 添加 `equipment` 表的全文搜索索引
- 优化价格查询相关索引
- 改进时间范围查询性能

#### 🗂️ 数据字典更新
- 完善JSON字段结构说明
- 更新字段注释和约束
- 添加外键关系图

---

### v2.0.0 (2024年12月)

#### 🆕 新增功能
- 重构整体数据库架构
- 添加装备管理模块
- 实现用户设备管理
- 增加路线评分系统

#### 🔧 核心表结构
- `users` - 用户基础信息表
- `cycling_routes` - 骑行路线表
- `cycling_records` - 骑行记录表
- `equipment` - 装备信息表
- `equipment_categories` - 装备分类表

#### 📊 关系设计
- 用户与路线的一对多关系
- 路线与记录的关联关系
- 装备分类的层级结构
- 用户互动功能（点赞、收藏、评分）

#### 🔒 安全特性
- 软删除机制
- 外键约束
- 数据完整性检查
- 审计字段（created_at, updated_at）

---

### v1.0.0 (2024年11月)

#### 🆕 初始版本
- 基础用户系统
- 简单路线管理
- 基本数据结构

---

## 🔄 迁移指南

### 从 v2.0.0 升级到 v2.1.0

1. **备份现有数据**
   ```sql
   mysqldump -u root -p ljxz > ljxz_backup_v2.0.0.sql
   ```

2. **执行升级脚本**
   ```sql
   -- 添加新字段和索引
   ALTER TABLE equipment ADD COLUMN color_options JSON DEFAULT NULL COMMENT '颜色选项';
   ALTER TABLE equipment ADD COLUMN size_options JSON DEFAULT NULL COMMENT '尺寸选项';
   
   -- 添加全文搜索索引
   ALTER TABLE equipment ADD FULLTEXT KEY ft_equipment_search (name, description, brand);
   ```

3. **验证升级结果**
   ```sql
   -- 检查表结构
   DESCRIBE equipment;
   
   -- 检查索引
   SHOW INDEX FROM equipment;
   ```

### 从 v1.0.0 升级到 v2.0.0

⚠️ **重要提示**: 这是一个重大版本升级，建议重新初始化数据库。

1. **导出重要数据**
2. **执行完整初始化脚本**
3. **重新导入数据**

---

## 📊 性能监控

### 关键指标
- 查询响应时间
- 索引使用率
- 表大小增长
- 慢查询统计

### 监控查询
```sql
-- 查看表大小
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'ljxz'
ORDER BY (data_length + index_length) DESC;

-- 查看索引使用情况
SELECT 
    table_schema,
    table_name,
    index_name,
    cardinality
FROM information_schema.statistics 
WHERE table_schema = 'ljxz'
ORDER BY cardinality DESC;
```

---

## 🔗 相关文档

- [数据库设计文档](../docs/DATABASE.md)
- [数据库设置指南](../vue-cycling-app/DATABASE_SETUP.md)
- [完整初始化脚本](./complete_init.sql)
- [测试数据脚本](./test_data.sql)

---

*最后更新时间：2025年1月*