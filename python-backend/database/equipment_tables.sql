-- 装备相关数据表
-- 在原有数据库基础上添加装备功能表

USE ljxz;

-- 装备分类表
CREATE TABLE IF NOT EXISTS equipment_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '分类名称',
    name_en VARCHAR(50) NOT NULL COMMENT '英文名称',
    description TEXT COMMENT '分类描述',
    parent_id INT COMMENT '父分类ID',
    sort_order INT DEFAULT 0 COMMENT '排序',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES equipment_categories(id) ON DELETE SET NULL
);

-- 装备表
CREATE TABLE IF NOT EXISTS equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL COMMENT '装备名称',
    brand VARCHAR(100) COMMENT '品牌',
    model VARCHAR(100) COMMENT '型号',
    category VARCHAR(50) NOT NULL COMMENT '分类',
    description TEXT COMMENT '装备描述',
    specifications JSON COMMENT '规格参数',
    images JSON COMMENT '图片URLs',
    tags JSON COMMENT '标签',
    weight FLOAT COMMENT '重量(克)',
    material VARCHAR(200) COMMENT '材质',
    color_options JSON COMMENT '颜色选项',
    size_options JSON COMMENT '尺寸选项',
    avg_rating DECIMAL(3,2) DEFAULT 0.00 COMMENT '平均评分',
    review_count INT DEFAULT 0 COMMENT '评价数量',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 装备价格表
CREATE TABLE IF NOT EXISTS equipment_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id BIGINT UNSIGNED NOT NULL COMMENT '装备ID',
    platform VARCHAR(50) NOT NULL COMMENT '平台名称',
    platform_url VARCHAR(500) COMMENT '商品链接',
    platform_id VARCHAR(100) COMMENT '平台商品ID',
    price DECIMAL(10,2) NOT NULL COMMENT '价格',
    original_price DECIMAL(10,2) COMMENT '原价',
    discount FLOAT COMMENT '折扣',
    currency VARCHAR(10) DEFAULT 'CNY' COMMENT '货币',
    stock_status VARCHAR(20) COMMENT '库存状态',
    seller_name VARCHAR(200) COMMENT '卖家名称',
    seller_rating DECIMAL(3,2) COMMENT '卖家评分',
    shipping_info JSON COMMENT '配送信息',
    promotion_info JSON COMMENT '促销信息',
    is_available BOOLEAN DEFAULT TRUE COMMENT '是否有货',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE
);

-- 装备标签表
CREATE TABLE IF NOT EXISTS equipment_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id BIGINT UNSIGNED NOT NULL COMMENT '装备ID',
    tag_name VARCHAR(50) NOT NULL COMMENT '标签名称',
    tag_type VARCHAR(20) DEFAULT 'custom' COMMENT '标签类型',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE
);

-- 装备评价表
CREATE TABLE IF NOT EXISTS equipment_reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id BIGINT UNSIGNED NOT NULL COMMENT '装备ID',
    platform VARCHAR(50) NOT NULL COMMENT '平台名称',
    platform_review_id VARCHAR(100) COMMENT '平台评价ID',
    user_name VARCHAR(100) COMMENT '用户名',
    user_avatar VARCHAR(500) COMMENT '用户头像',
    rating INT NOT NULL COMMENT '评分(1-5)',
    title VARCHAR(200) COMMENT '评价标题',
    content TEXT COMMENT '评价内容',
    images JSON COMMENT '评价图片',
    purchase_info JSON COMMENT '购买信息',
    helpful_count INT DEFAULT 0 COMMENT '有用数',
    reply_count INT DEFAULT 0 COMMENT '回复数',
    is_verified BOOLEAN DEFAULT FALSE COMMENT '是否认证购买',
    review_date DATETIME COMMENT '评价时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE,
    CHECK (rating >= 1 AND rating <= 5)
);

-- 用户装备收藏表
CREATE TABLE IF NOT EXISTS user_equipment_favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '用户ID',
    equipment_id BIGINT UNSIGNED NOT NULL COMMENT '装备ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_equipment (user_id, equipment_id)
);

-- 价格提醒表
CREATE TABLE IF NOT EXISTS price_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '用户ID',
    equipment_id BIGINT UNSIGNED NOT NULL COMMENT '装备ID',
    target_price DECIMAL(10,2) NOT NULL COMMENT '目标价格',
    platform VARCHAR(50) COMMENT '指定平台',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    last_check_time TIMESTAMP COMMENT '最后检查时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE
);

-- 创建索引以提高查询性能
CREATE INDEX idx_equipment_name ON equipment(name);
CREATE INDEX idx_equipment_brand ON equipment(brand);
CREATE INDEX idx_equipment_category ON equipment(category);
CREATE INDEX idx_equipment_rating ON equipment(avg_rating);
CREATE INDEX idx_equipment_created ON equipment(created_at);

CREATE INDEX idx_price_equipment ON equipment_prices(equipment_id);
CREATE INDEX idx_price_platform ON equipment_prices(platform);
CREATE INDEX idx_price_created ON equipment_prices(created_at);
CREATE INDEX idx_price_equipment_platform ON equipment_prices(equipment_id, platform);
CREATE INDEX idx_price_value ON equipment_prices(price);

CREATE INDEX idx_review_equipment ON equipment_reviews(equipment_id);
CREATE INDEX idx_review_platform ON equipment_reviews(platform);
CREATE INDEX idx_review_rating ON equipment_reviews(rating);
CREATE INDEX idx_review_date ON equipment_reviews(review_date);

CREATE INDEX idx_favorites_user ON user_equipment_favorites(user_id);
CREATE INDEX idx_favorites_equipment ON user_equipment_favorites(equipment_id);

CREATE INDEX idx_alerts_user ON price_alerts(user_id);
CREATE INDEX idx_alerts_equipment ON price_alerts(equipment_id);
CREATE INDEX idx_alerts_active ON price_alerts(is_active);

-- 插入初始装备分类数据
INSERT INTO equipment_categories (name, name_en, description, sort_order) VALUES
('自行车', 'bikes', '各类自行车整车', 1),
('骑行服装', 'clothing', '骑行专用服装装备', 2),
('安全防护', 'safety', '头盔、护具等安全装备', 3),
('骑行配件', 'accessories', '车灯、码表、水壶等配件', 4),
('自行车零件', 'parts', '轮胎、刹车、变速器等零部件', 5),
('维修工具', 'tools', '打气筒、工具包等维修工具', 6);

-- 插入自行车子分类
INSERT INTO equipment_categories (name, name_en, description, parent_id, sort_order) VALUES
('山地车', 'mountain-bikes', '适合山地骑行的自行车', 1, 1),
('公路车', 'road-bikes', '适合公路骑行的自行车', 1, 2),
('折叠车', 'folding-bikes', '可折叠便携自行车', 1, 3),
('电动车', 'electric-bikes', '电动助力自行车', 1, 4),
('城市车', 'city-bikes', '适合城市通勤的自行车', 1, 5);

-- 插入骑行服装子分类
INSERT INTO equipment_categories (name, name_en, description, parent_id, sort_order) VALUES
('骑行上衣', 'cycling-jerseys', '骑行专用上衣', 2, 1),
('骑行裤', 'cycling-shorts', '骑行专用裤子', 2, 2),
('骑行手套', 'cycling-gloves', '骑行专用手套', 2, 3),
('骑行鞋', 'cycling-shoes', '骑行专用鞋子', 2, 4),
('骑行袜', 'cycling-socks', '骑行专用袜子', 2, 5);

-- 插入安全防护子分类
INSERT INTO equipment_categories (name, name_en, description, parent_id, sort_order) VALUES
('头盔', 'helmets', '骑行安全头盔', 3, 1),
('护膝护肘', 'knee-elbow-pads', '膝盖和肘部护具', 3, 2),
('反光装备', 'reflective-gear', '反光背心、臂带等', 3, 3);

-- 插入骑行配件子分类
INSERT INTO equipment_categories (name, name_en, description, parent_id, sort_order) VALUES
('车灯', 'bike-lights', '前灯、尾灯等照明设备', 4, 1),
('码表', 'bike-computers', '速度、距离等数据记录设备', 4, 2),
('水壶架', 'bottle-cages', '水壶固定架', 4, 3),
('车锁', 'bike-locks', '自行车防盗锁', 4, 4),
('车包', 'bike-bags', '车前包、车后包等储物装备', 4, 5);

COMMIT;