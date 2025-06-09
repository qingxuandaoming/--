-- 灵境行者数据库完整初始化脚本
-- 创建时间：2025年1月
-- 版本：v2.1.0
-- 更新时间：2025年1月
-- 描述：包含用户系统、骑行路线、装备管理等完整功能的数据库结构

-- 创建数据库
CREATE DATABASE IF NOT EXISTS ljxz CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE ljxz;

-- 设置时区
SET time_zone = '+08:00';

-- ============================================
-- 核心用户表
-- ============================================

-- Users table
CREATE TABLE IF NOT EXISTS `users` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'User ID',
  `email` VARCHAR(255) NOT NULL COMMENT 'Email address',
  `username` VARCHAR(50) NOT NULL COMMENT 'Username',
  `password_hash` VARCHAR(255) NOT NULL COMMENT 'Password hash',
  `nickname` VARCHAR(50) DEFAULT NULL COMMENT 'Nickname',
  `phone` VARCHAR(20) DEFAULT NULL COMMENT 'Phone number',
  `avatar_url` VARCHAR(500) DEFAULT NULL COMMENT 'Avatar URL',
  `status` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态：1-正常，0-禁用',
  `email_verified_at` TIMESTAMP NULL DEFAULT NULL COMMENT '邮箱验证时间',
  `last_login_at` TIMESTAMP NULL DEFAULT NULL COMMENT '最后登录时间',
  `login_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '登录次数',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_at` TIMESTAMP NULL DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_users_email` (`email`),
  UNIQUE KEY `uk_users_username` (`username`),
  KEY `idx_users_phone` (`phone`),
  KEY `idx_users_status` (`status`),
  KEY `idx_users_created_at` (`created_at`),
  KEY `idx_users_deleted_at` (`deleted_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ============================================
-- 骑行相关表
-- ============================================

-- 骑行路线表
CREATE TABLE IF NOT EXISTS `cycling_routes` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '路线ID',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '创建用户ID',
  `name` VARCHAR(100) NOT NULL COMMENT '路线名称',
  `description` TEXT DEFAULT NULL COMMENT '路线描述',
  `start_latitude` DECIMAL(10,7) NOT NULL COMMENT '起点纬度',
  `start_longitude` DECIMAL(10,7) NOT NULL COMMENT '起点经度',
  `start_address` VARCHAR(255) DEFAULT NULL COMMENT '起点地址',
  `end_latitude` DECIMAL(10,7) NOT NULL COMMENT '终点纬度',
  `end_longitude` DECIMAL(10,7) NOT NULL COMMENT '终点经度',
  `end_address` VARCHAR(255) DEFAULT NULL COMMENT '终点地址',
  `waypoints` JSON DEFAULT NULL COMMENT '途经点坐标',
  `difficulty` ENUM('EASY','MEDIUM','HARD') NOT NULL DEFAULT 'MEDIUM' COMMENT '难度等级',
  `estimated_time` INT UNSIGNED DEFAULT NULL COMMENT '预计用时（分钟）',
  `distance` DECIMAL(8,2) DEFAULT NULL COMMENT '距离（公里）',
  `elevation_gain` DECIMAL(8,2) DEFAULT NULL COMMENT '爬升高度（米）',
  `tags` JSON DEFAULT NULL COMMENT '标签',
  `is_public` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否公开：1-公开，0-私有',
  `view_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '浏览次数',
  `like_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '点赞次数',
  `city` VARCHAR(50) DEFAULT NULL COMMENT '所在城市',
  `province` VARCHAR(50) DEFAULT NULL COMMENT '所在省份',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_at` TIMESTAMP NULL DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`),
  KEY `fk_routes_users` (`user_id`),
  KEY `idx_routes_difficulty` (`difficulty`),
  KEY `idx_routes_distance` (`distance`),
  KEY `idx_routes_city` (`city`),
  KEY `idx_routes_is_public` (`is_public`),
  KEY `idx_routes_created_at` (`created_at`),
  KEY `idx_routes_deleted_at` (`deleted_at`),
  CONSTRAINT `fk_routes_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='骑行路线表';

-- 骑行记录表
CREATE TABLE IF NOT EXISTS `cycling_records` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  `route_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '路线ID',
  `start_latitude` DECIMAL(10,7) NOT NULL COMMENT '起点纬度',
  `start_longitude` DECIMAL(10,7) NOT NULL COMMENT '起点经度',
  `end_latitude` DECIMAL(10,7) DEFAULT NULL COMMENT '终点纬度',
  `end_longitude` DECIMAL(10,7) DEFAULT NULL COMMENT '终点经度',
  `total_distance` DECIMAL(8,2) DEFAULT NULL COMMENT '总距离（公里）',
  `total_time` INT UNSIGNED DEFAULT NULL COMMENT '总用时（秒）',
  `average_speed` DECIMAL(5,2) DEFAULT NULL COMMENT '平均速度（km/h）',
  `max_speed` DECIMAL(5,2) DEFAULT NULL COMMENT '最高速度（km/h）',
  `calories` INT UNSIGNED DEFAULT NULL COMMENT '消耗卡路里',
  `elevation_gain` DECIMAL(8,2) DEFAULT NULL COMMENT '爬升高度（米）',
  `gps_data` JSON DEFAULT NULL COMMENT 'GPS轨迹数据',
  `heart_rate_data` JSON DEFAULT NULL COMMENT '心率数据',
  `power_data` JSON DEFAULT NULL COMMENT '功率数据',
  `weather_data` JSON DEFAULT NULL COMMENT '天气数据',
  `start_time` TIMESTAMP NOT NULL COMMENT '开始时间',
  `end_time` TIMESTAMP DEFAULT NULL COMMENT '结束时间',
  `status` ENUM('STARTED','PAUSED','COMPLETED','CANCELLED') NOT NULL DEFAULT 'STARTED' COMMENT '状态',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `fk_records_users` (`user_id`),
  KEY `fk_records_routes` (`route_id`),
  KEY `idx_records_start_time` (`start_time`),
  KEY `idx_records_status` (`status`),
  KEY `idx_records_distance` (`total_distance`),
  KEY `idx_records_created_at` (`created_at`),
  CONSTRAINT `fk_records_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_records_routes` FOREIGN KEY (`route_id`) REFERENCES `cycling_routes` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='骑行记录表';

-- 路线点赞表
CREATE TABLE IF NOT EXISTS `route_likes` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  `route_id` BIGINT UNSIGNED NOT NULL COMMENT '路线ID',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_route_likes` (`user_id`, `route_id`),
  KEY `fk_route_likes_users` (`user_id`),
  KEY `fk_route_likes_routes` (`route_id`),
  CONSTRAINT `fk_route_likes_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_route_likes_routes` FOREIGN KEY (`route_id`) REFERENCES `cycling_routes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='路线点赞表';

-- 路线收藏表
CREATE TABLE IF NOT EXISTS `route_favorites` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  `route_id` BIGINT UNSIGNED NOT NULL COMMENT '路线ID',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_route_favorites` (`user_id`, `route_id`),
  KEY `fk_route_favorites_users` (`user_id`),
  KEY `fk_route_favorites_routes` (`route_id`),
  CONSTRAINT `fk_route_favorites_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_route_favorites_routes` FOREIGN KEY (`route_id`) REFERENCES `cycling_routes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='路线收藏表';

-- 路线评分表
CREATE TABLE IF NOT EXISTS `route_ratings` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  `route_id` BIGINT UNSIGNED NOT NULL COMMENT '路线ID',
  `rating` INT NOT NULL COMMENT '评分（1-5）',
  `comment` TEXT DEFAULT NULL COMMENT '评价内容',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_route_ratings` (`user_id`, `route_id`),
  KEY `fk_route_ratings_users` (`user_id`),
  KEY `fk_route_ratings_routes` (`route_id`),
  KEY `idx_route_ratings_rating` (`rating`),
  CONSTRAINT `fk_route_ratings_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_route_ratings_routes` FOREIGN KEY (`route_id`) REFERENCES `cycling_routes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `chk_rating_range` CHECK (`rating` >= 1 AND `rating` <= 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='路线评分表';

-- ============================================
-- 设备装备相关表
-- ============================================

-- 装备分类表
CREATE TABLE IF NOT EXISTS `equipment_categories` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分类ID',
  `name` VARCHAR(50) NOT NULL COMMENT '分类名称',
  `name_en` VARCHAR(50) NOT NULL COMMENT '英文名称',
  `description` TEXT DEFAULT NULL COMMENT '分类描述',
  `parent_id` INT UNSIGNED DEFAULT NULL COMMENT '父分类ID',
  `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_categories_name` (`name`),
  KEY `fk_categories_parent` (`parent_id`),
  KEY `idx_categories_sort` (`sort_order`),
  KEY `idx_categories_active` (`is_active`),
  CONSTRAINT `fk_categories_parent` FOREIGN KEY (`parent_id`) REFERENCES `equipment_categories` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='装备分类表';

-- 装备表
CREATE TABLE IF NOT EXISTS `equipment` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '设备ID',
  `name` VARCHAR(255) NOT NULL COMMENT '设备名称',
  `category_id` INT UNSIGNED NOT NULL COMMENT '分类ID',
  `subcategory` VARCHAR(50) DEFAULT NULL COMMENT '子类别',
  `brand` VARCHAR(100) NOT NULL COMMENT '品牌',
  `model` VARCHAR(100) DEFAULT NULL COMMENT '型号',
  `price` DECIMAL(10,2) DEFAULT NULL COMMENT '当前价格',
  `original_price` DECIMAL(10,2) DEFAULT NULL COMMENT '原价',
  `discount` DECIMAL(3,2) DEFAULT NULL COMMENT '折扣率',
  `description` TEXT DEFAULT NULL COMMENT '描述',
  `detailed_description` LONGTEXT DEFAULT NULL COMMENT '详细描述',
  `specifications` JSON DEFAULT NULL COMMENT '规格参数',
  `images` JSON DEFAULT NULL COMMENT '图片URLs',
  `tags` JSON DEFAULT NULL COMMENT '标签',
  `weight` FLOAT DEFAULT NULL COMMENT '重量(克)',
  `material` VARCHAR(200) DEFAULT NULL COMMENT '材质',
  `color_options` JSON DEFAULT NULL COMMENT '颜色选项',
  `size_options` JSON DEFAULT NULL COMMENT '尺寸选项',
  `availability` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否有货',
  `stock` INT UNSIGNED DEFAULT NULL COMMENT '库存数量',
  `rating` DECIMAL(3,2) DEFAULT NULL COMMENT '评分',
  `review_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '评价数量',
  `sales_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '销量',
  `source` VARCHAR(50) NOT NULL COMMENT '数据来源',
  `source_url` VARCHAR(500) DEFAULT NULL COMMENT '来源URL',
  `source_id` VARCHAR(100) DEFAULT NULL COMMENT '来源商品ID',
  `last_updated` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_equipment_source` (`source`, `source_id`),
  KEY `fk_equipment_category` (`category_id`),
  KEY `idx_equipment_brand` (`brand`),
  KEY `idx_equipment_price` (`price`),
  KEY `idx_equipment_rating` (`rating`),
  KEY `idx_equipment_availability` (`availability`),
  KEY `idx_equipment_last_updated` (`last_updated`),
  FULLTEXT KEY `ft_equipment_search` (`name`, `description`, `brand`),
  CONSTRAINT `fk_equipment_category` FOREIGN KEY (`category_id`) REFERENCES `equipment_categories` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='设备信息表';

-- 设备价格历史表
CREATE TABLE IF NOT EXISTS `equipment_price_history` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `equipment_id` BIGINT UNSIGNED NOT NULL COMMENT '设备ID',
  `price` DECIMAL(10,2) NOT NULL COMMENT '价格',
  `original_price` DECIMAL(10,2) DEFAULT NULL COMMENT '原价',
  `discount` DECIMAL(3,2) DEFAULT NULL COMMENT '折扣率',
  `availability` TINYINT(1) NOT NULL COMMENT '是否有货',
  `stock` INT UNSIGNED DEFAULT NULL COMMENT '库存数量',
  `recorded_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
  PRIMARY KEY (`id`),
  KEY `fk_price_history_equipment` (`equipment_id`),
  KEY `idx_price_history_recorded_at` (`recorded_at`),
  KEY `idx_price_history_price` (`price`),
  CONSTRAINT `fk_price_history_equipment` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='设备价格历史表';

-- 用户设备收藏表
CREATE TABLE IF NOT EXISTS `user_equipment_favorites` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  `equipment_id` BIGINT UNSIGNED NOT NULL COMMENT '设备ID',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_equipment_favorites` (`user_id`, `equipment_id`),
  KEY `fk_user_equipment_favorites_users` (`user_id`),
  KEY `fk_user_equipment_favorites_equipment` (`equipment_id`),
  CONSTRAINT `fk_user_equipment_favorites_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_user_equipment_favorites_equipment` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户设备收藏表';

-- 价格提醒表
CREATE TABLE IF NOT EXISTS `price_alerts` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  `equipment_id` BIGINT UNSIGNED NOT NULL COMMENT '设备ID',
  `target_price` DECIMAL(10,2) NOT NULL COMMENT '目标价格',
  `platform` VARCHAR(50) DEFAULT NULL COMMENT '指定平台',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
  `last_check_time` TIMESTAMP NULL DEFAULT NULL COMMENT '最后检查时间',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `fk_price_alerts_users` (`user_id`),
  KEY `fk_price_alerts_equipment` (`equipment_id`),
  KEY `idx_price_alerts_active` (`is_active`),
  CONSTRAINT `fk_price_alerts_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_price_alerts_equipment` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='价格提醒表';

-- ============================================
-- 设备管理相关表
-- ============================================

-- 用户设备表
CREATE TABLE IF NOT EXISTS `user_devices` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  `device_id` VARCHAR(100) NOT NULL COMMENT '设备唯一标识',
  `device_type` ENUM('BIKE_COMPUTER','HEART_RATE_MONITOR','POWER_METER','SMART_TRAINER','MOBILE_APP') NOT NULL COMMENT '设备类型',
  `device_name` VARCHAR(100) NOT NULL COMMENT '设备名称',
  `manufacturer` VARCHAR(50) DEFAULT NULL COMMENT '制造商',
  `model` VARCHAR(50) DEFAULT NULL COMMENT '型号',
  `firmware_version` VARCHAR(20) DEFAULT NULL COMMENT '固件版本',
  `settings` JSON DEFAULT NULL COMMENT '设备设置',
  `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否激活',
  `last_sync` TIMESTAMP NULL DEFAULT NULL COMMENT '最后同步时间',
  `sync_count` INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '同步次数',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_devices` (`user_id`, `device_id`),
  KEY `fk_user_devices_users` (`user_id`),
  KEY `idx_user_devices_type` (`device_type`),
  KEY `idx_user_devices_active` (`is_active`),
  CONSTRAINT `fk_user_devices_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户设备表';

-- ============================================
-- 爬虫系统相关表
-- ============================================

-- 爬虫任务表
CREATE TABLE IF NOT EXISTS `crawler_tasks` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '任务ID',
  `task_id` VARCHAR(50) NOT NULL COMMENT '任务唯一标识',
  `task_type` ENUM('FULL_CRAWL','INCREMENTAL_CRAWL','PRICE_UPDATE') NOT NULL COMMENT '任务类型',
  `sources` JSON NOT NULL COMMENT '爬取来源',
  `categories` JSON DEFAULT NULL COMMENT '爬取类别',
  `status` ENUM('PENDING','RUNNING','COMPLETED','FAILED','CANCELLED') NOT NULL DEFAULT 'PENDING' COMMENT '任务状态',
  `progress` JSON DEFAULT NULL COMMENT '进度信息',
  `results` JSON DEFAULT NULL COMMENT '结果统计',
  `error_message` TEXT DEFAULT NULL COMMENT '错误信息',
  `start_time` TIMESTAMP NULL DEFAULT NULL COMMENT '开始时间',
  `end_time` TIMESTAMP NULL DEFAULT NULL COMMENT '结束时间',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_crawler_tasks_task_id` (`task_id`),
  KEY `idx_crawler_tasks_status` (`status`),
  KEY `idx_crawler_tasks_type` (`task_type`),
  KEY `idx_crawler_tasks_start_time` (`start_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='爬虫任务表';

-- ============================================
-- 系统管理相关表
-- ============================================

-- 用户反馈表
CREATE TABLE IF NOT EXISTS `feedback` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '反馈ID',
  `user_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '用户ID',
  `subject` VARCHAR(200) NOT NULL COMMENT '主题',
  `message` TEXT NOT NULL COMMENT '反馈内容',
  `contact_email` VARCHAR(100) DEFAULT NULL COMMENT '联系邮箱',
  `status` ENUM('PENDING','IN_PROGRESS','RESOLVED','CLOSED') NOT NULL DEFAULT 'PENDING' COMMENT '状态',
  `admin_reply` TEXT DEFAULT NULL COMMENT '管理员回复',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `fk_feedback_users` (`user_id`),
  KEY `idx_feedback_status` (`status`),
  KEY `idx_feedback_created_at` (`created_at`),
  CONSTRAINT `fk_feedback_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户反馈表';

-- ============================================
-- 插入初始数据
-- ============================================

-- 插入管理员用户
INSERT INTO `users` (`email`, `username`, `password_hash`, `nickname`, `phone`, `status`) VALUES
('admin@ljxz.com', 'admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', '系统管理员', '13800138000', 1),
('test@ljxz.com', 'testuser', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', '测试用户', '13900139000', 1),
('demo@ljxz.com', 'demo', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', '演示用户', '13700137000', 1);

-- 插入装备分类数据
INSERT INTO `equipment_categories` (`name`, `name_en`, `description`, `sort_order`) VALUES
('自行车', 'bikes', '各类自行车整车', 1),
('骑行服装', 'clothing', '骑行专用服装装备', 2),
('安全防护', 'safety', '头盔、护具等安全装备', 3),
('骑行配件', 'accessories', '车灯、码表、水壶等配件', 4),
('自行车零件', 'parts', '轮胎、刹车、变速器等零部件', 5),
('维修工具', 'tools', '打气筒、工具包等维修工具', 6);

-- 插入自行车子分类
INSERT INTO `equipment_categories` (`name`, `name_en`, `description`, `parent_id`, `sort_order`) VALUES
('山地车', 'mountain-bikes', '适合山地骑行的自行车', 1, 1),
('公路车', 'road-bikes', '适合公路骑行的自行车', 1, 2),
('折叠车', 'folding-bikes', '可折叠便携自行车', 1, 3),
('电动车', 'electric-bikes', '电动助力自行车', 1, 4),
('城市车', 'city-bikes', '适合城市通勤的自行车', 1, 5);

-- 插入骑行服装子分类
INSERT INTO `equipment_categories` (`name`, `name_en`, `description`, `parent_id`, `sort_order`) VALUES
('骑行上衣', 'cycling-jerseys', '骑行专用上衣', 2, 1),
('骑行裤', 'cycling-shorts', '骑行专用裤子', 2, 2),
('骑行手套', 'cycling-gloves', '骑行专用手套', 2, 3),
('骑行鞋', 'cycling-shoes', '骑行专用鞋子', 2, 4),
('骑行袜', 'cycling-socks', '骑行专用袜子', 2, 5);

-- 插入安全防护子分类
INSERT INTO `equipment_categories` (`name`, `name_en`, `description`, `parent_id`, `sort_order`) VALUES
('头盔', 'helmets', '骑行安全头盔', 3, 1),
('护膝护肘', 'knee-elbow-pads', '膝盖和肘部护具', 3, 2),
('反光装备', 'reflective-gear', '反光背心、臂带等', 3, 3);

-- 插入骑行配件子分类
INSERT INTO `equipment_categories` (`name`, `name_en`, `description`, `parent_id`, `sort_order`) VALUES
('车灯', 'bike-lights', '前灯、尾灯等照明设备', 4, 1),
('码表', 'bike-computers', '速度、距离等数据记录设备', 4, 2),
('水壶架', 'bottle-cages', '水壶固定架', 4, 3),
('车锁', 'bike-locks', '自行车防盗锁', 4, 4),
('车包', 'bike-bags', '车前包、车后包等储物装备', 4, 5);

-- 插入示例骑行路线
INSERT INTO `cycling_routes` (`user_id`, `name`, `description`, `start_latitude`, `start_longitude`, `start_address`, `end_latitude`, `end_longitude`, `end_address`, `difficulty`, `estimated_time`, `distance`, `elevation_gain`, `city`, `province`, `tags`) VALUES
(1, '西湖环线经典路线', '杭州西湖最经典的骑行路线，沿湖而行，风景优美，适合休闲骑行', 30.2741, 120.1551, '杭州市西湖区断桥残雪', 30.2441, 120.1351, '杭州市西湖区雷峰塔', 'EASY', 90, 12.5, 50, '杭州', '浙江', '["休闲", "风景", "初学者友好"]'),
(1, '千岛湖环湖挑战', '千岛湖风景区环湖骑行，路程较长，有一定挑战性', 29.6050, 119.0350, '淳安县千岛湖镇', 29.6050, 119.0350, '淳安县千岛湖镇', 'MEDIUM', 240, 38.2, 320, '杭州', '浙江', '["挑战", "环湖", "风景"]'),
(2, '钱塘江沿岸骑行', '沿钱塘江骑行，可欣赏江景和城市风光', 30.2467, 120.2103, '杭州市滨江区钱塘江边', 30.2890, 120.1552, '杭州市上城区钱塘江边', 'EASY', 75, 15.8, 30, '杭州', '浙江', '["江景", "城市", "平坦"]'),
(2, '径山古道探险', '历史悠久的径山古道，山路崎岖，适合山地车', 30.3456, 119.9876, '余杭区径山镇', 30.3789, 119.9543, '径山寺', 'HARD', 180, 22.6, 650, '杭州', '浙江', '["古道", "山地", "历史"]'),
(3, '运河文化骑行', '沿京杭大运河骑行，感受运河文化', 30.2776, 120.1234, '拱墅区运河广场', 30.3123, 120.1567, '塘栖古镇', 'MEDIUM', 120, 18.9, 80, '杭州', '浙江', '["文化", "运河", "古镇"]');

-- 插入示例设备数据
INSERT INTO `equipment` (`name`, `category_id`, `brand`, `model`, `price`, `original_price`, `description`, `specifications`, `images`, `availability`, `source`, `source_url`) VALUES
('捷安特 ATX 810 山地车', 7, '捷安特', 'ATX 810', 2998.00, 3298.00, '入门级山地车，适合城市骑行和轻度越野', '{"frame": "铝合金车架", "wheelSize": "27.5寸", "gears": "21速", "weight": "13.5kg", "brakes": "机械碟刹"}', '["https://example.com/bike1.jpg", "https://example.com/bike1_2.jpg"]', 1, '京东', 'https://item.jd.com/example1.html'),
('美利达 公爵 600 山地车', 7, '美利达', '公爵 600', 1998.00, 2298.00, '性价比山地车，适合新手入门', '{"frame": "铝合金车架", "wheelSize": "26寸", "gears": "18速", "weight": "14.2kg", "brakes": "V刹"}', '["https://example.com/bike2.jpg"]', 1, '天猫', 'https://detail.tmall.com/example2.html'),
('闪电 Allez Elite 公路车', 8, '闪电', 'Allez Elite', 8999.00, 9999.00, '专业级公路车，适合竞技和长途骑行', '{"frame": "碳纤维车架", "wheelSize": "700C", "gears": "22速", "weight": "8.9kg", "brakes": "碟刹"}', '["https://example.com/bike3.jpg", "https://example.com/bike3_2.jpg"]', 1, '官网', 'https://specialized.com/example3.html'),
('Giro Syntax MIPS 头盔', 16, 'Giro', 'Syntax MIPS', 899.00, 1099.00, '专业骑行头盔，MIPS技术提供更好保护', '{"weight": "280g", "vents": "25个通风孔", "technology": "MIPS", "sizes": ["S", "M", "L"]}', '["https://example.com/helmet1.jpg"]', 1, '京东', 'https://item.jd.com/helmet1.html'),
('Garmin Edge 530 码表', 21, 'Garmin', 'Edge 530', 2299.00, 2599.00, '专业GPS骑行码表，支持导航和训练分析', '{"screen": "2.6寸彩屏", "battery": "20小时", "gps": "GPS+GLONASS+Galileo", "waterproof": "IPX7"}', '["https://example.com/computer1.jpg"]', 1, '天猫', 'https://detail.tmall.com/computer1.html');

-- 插入示例骑行记录
INSERT INTO `cycling_records` (`user_id`, `route_id`, `start_latitude`, `start_longitude`, `end_latitude`, `end_longitude`, `total_distance`, `total_time`, `average_speed`, `max_speed`, `calories`, `elevation_gain`, `start_time`, `end_time`, `status`) VALUES
(2, 1, 30.2741, 120.1551, 30.2441, 120.1351, 12.3, 5280, 14.2, 28.5, 420, 48, '2025-01-15 08:30:00', '2025-01-15 10:18:00', 'COMPLETED'),
(3, 1, 30.2741, 120.1551, 30.2441, 120.1351, 12.1, 4920, 14.8, 31.2, 380, 52, '2025-01-16 09:15:00', '2025-01-16 11:07:00', 'COMPLETED'),
(2, 3, 30.2467, 120.2103, 30.2890, 120.1552, 15.6, 4200, 13.4, 26.8, 510, 28, '2025-01-17 07:45:00', '2025-01-17 08:55:00', 'COMPLETED'),
(3, 2, 29.6050, 119.0350, 29.6050, 119.0350, 36.8, 8640, 15.3, 42.1, 1280, 315, '2025-01-18 06:00:00', '2025-01-18 08:24:00', 'COMPLETED');

-- 插入路线点赞数据
INSERT INTO `route_likes` (`user_id`, `route_id`) VALUES
(2, 1), (3, 1), (2, 3), (3, 2), (1, 3);

-- 插入路线收藏数据
INSERT INTO `route_favorites` (`user_id`, `route_id`) VALUES
(2, 1), (2, 2), (3, 1), (3, 3), (1, 4);

-- 插入路线评分数据
INSERT INTO `route_ratings` (`user_id`, `route_id`, `rating`, `comment`) VALUES
(2, 1, 5, '非常棒的路线，风景优美，路况良好，强烈推荐！'),
(3, 1, 4, '很不错的休闲路线，适合周末骑行，就是人有点多'),
(2, 3, 4, '沿江风景不错，路比较平坦，适合新手'),
(3, 2, 5, '挑战性很强的路线，风景绝美，值得一试！');

-- 插入设备收藏数据
INSERT INTO `user_equipment_favorites` (`user_id`, `equipment_id`) VALUES
(2, 1), (2, 4), (3, 1), (3, 3), (3, 5);

-- 插入价格提醒数据
INSERT INTO `price_alerts` (`user_id`, `equipment_id`, `target_price`) VALUES
(2, 1, 2500.00), (3, 3, 8000.00), (2, 5, 2000.00);

-- 插入用户设备数据
INSERT INTO `user_devices` (`user_id`, `device_id`, `device_type`, `device_name`, `manufacturer`, `model`) VALUES
(2, 'GARMIN_530_001', 'BIKE_COMPUTER', 'Garmin Edge 530', 'Garmin', 'Edge 530'),
(3, 'POLAR_H10_002', 'HEART_RATE_MONITOR', 'Polar H10心率带', 'Polar', 'H10'),
(2, 'IPHONE_APP_001', 'MOBILE_APP', 'iPhone 骑行应用', 'Apple', 'iPhone 13');

-- 更新路线统计数据
UPDATE `cycling_routes` SET 
  `like_count` = (SELECT COUNT(*) FROM `route_likes` WHERE `route_id` = `cycling_routes`.`id`),
  `view_count` = FLOOR(RAND() * 100) + 50
WHERE `id` IN (1, 2, 3, 4, 5);

COMMIT;

-- ============================================
-- 创建触发器
-- ============================================

DELIMITER //

-- 路线点赞触发器
CREATE TRIGGER tr_route_like_insert
AFTER INSERT ON route_likes
FOR EACH ROW
BEGIN
    UPDATE cycling_routes 
    SET like_count = like_count + 1 
    WHERE id = NEW.route_id;
END //

CREATE TRIGGER tr_route_like_delete
AFTER DELETE ON route_likes
FOR EACH ROW
BEGIN
    UPDATE cycling_routes 
    SET like_count = like_count - 1 
    WHERE id = OLD.route_id;
END //

-- 设备价格历史触发器
CREATE TRIGGER tr_equipment_price_update
AFTER UPDATE ON equipment
FOR EACH ROW
BEGIN
    IF OLD.price != NEW.price OR OLD.availability != NEW.availability THEN
        INSERT INTO equipment_price_history (
            equipment_id, price, original_price, discount, 
            availability, stock, recorded_at
        ) VALUES (
            NEW.id, NEW.price, NEW.original_price, NEW.discount,
            NEW.availability, NEW.stock, NOW()
        );
    END IF;
END //

DELIMITER ;

-- ============================================
-- 创建视图
-- ============================================

-- 热门路线视图
CREATE VIEW v_popular_routes AS
SELECT 
    cr.id,
    cr.name,
    cr.description,
    cr.difficulty,
    cr.distance,
    cr.estimated_time,
    cr.city,
    cr.like_count,
    cr.view_count,
    u.nickname as creator_name,
    COUNT(rec.id) as completion_count,
    AVG(rec.total_time) as avg_completion_time,
    AVG(rr.rating) as avg_rating,
    cr.created_at
FROM cycling_routes cr
JOIN users u ON cr.user_id = u.id
LEFT JOIN cycling_records rec ON cr.id = rec.route_id AND rec.status = 'COMPLETED'
LEFT JOIN route_ratings rr ON cr.id = rr.route_id
WHERE cr.is_public = 1 AND cr.deleted_at IS NULL
GROUP BY cr.id, cr.name, cr.description, cr.difficulty, cr.distance, 
         cr.estimated_time, cr.city, cr.like_count, cr.view_count, 
         u.nickname, cr.created_at
ORDER BY (cr.like_count * 0.4 + cr.view_count * 0.3 + COUNT(rec.id) * 0.3) DESC;

-- 用户统计视图
CREATE VIEW v_user_stats AS
SELECT 
    u.id,
    u.nickname,
    COUNT(DISTINCT cr.id) as total_routes,
    COUNT(DISTINCT rec.id) as total_records,
    COALESCE(SUM(rec.total_distance), 0) as total_distance,
    COALESCE(SUM(rec.total_time), 0) as total_time,
    COALESCE(AVG(rec.average_speed), 0) as avg_speed,
    COALESCE(SUM(rec.calories), 0) as total_calories,
    COUNT(DISTINCT rl.id) as total_likes_given,
    COUNT(DISTINCT rf.id) as total_favorites
FROM users u
LEFT JOIN cycling_routes cr ON u.id = cr.user_id AND cr.deleted_at IS NULL
LEFT JOIN cycling_records rec ON u.id = rec.user_id AND rec.status = 'COMPLETED'
LEFT JOIN route_likes rl ON u.id = rl.user_id
LEFT JOIN route_favorites rf ON u.id = rf.user_id
WHERE u.deleted_at IS NULL
GROUP BY u.id, u.nickname;

SELECT 'Database initialization completed successfully!' as message;