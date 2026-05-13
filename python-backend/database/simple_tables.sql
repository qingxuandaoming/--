-- 简化的装备数据库表结构

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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 装备表
CREATE TABLE IF NOT EXISTS equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL COMMENT '装备名称',
    brand VARCHAR(100) COMMENT '品牌',
    model VARCHAR(100) COMMENT '型号',
    category VARCHAR(50) NOT NULL COMMENT '分类',
    subcategory VARCHAR(50) COMMENT '子分类',
    price FLOAT COMMENT '价格',
    currency VARCHAR(10) DEFAULT 'CNY' COMMENT '货币',
    description TEXT COMMENT '装备描述',
    specifications JSON COMMENT '规格参数',
    image_urls JSON COMMENT '装备图片',
    purchase_urls JSON COMMENT '购买链接',
    rating_avg DECIMAL(3,2) DEFAULT 0.00 COMMENT '平均评分',
    rating_count INT DEFAULT 0 COMMENT '评价数量',
    view_count INT DEFAULT 0 COMMENT '浏览次数',
    favorite_count INT DEFAULT 0 COMMENT '收藏次数',
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 装备价格表
CREATE TABLE IF NOT EXISTS equipment_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT NOT NULL COMMENT '装备ID',
    platform VARCHAR(50) NOT NULL COMMENT '平台名称',
    platform_url VARCHAR(500) COMMENT '商品链接',
    platform_id VARCHAR(100) COMMENT '平台商品ID',
    price DECIMAL(10,2) NOT NULL COMMENT '价格',
    original_price DECIMAL(10,2) COMMENT '原价',
    discount_rate DECIMAL(5,2) COMMENT '折扣率',
    currency VARCHAR(10) DEFAULT 'CNY' COMMENT '货币',
    is_available BOOLEAN DEFAULT TRUE COMMENT '是否有货',
    shipping_fee DECIMAL(10,2) COMMENT '运费',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入基础分类数据
INSERT IGNORE INTO equipment_categories (name, name_en, description) VALUES
('山地车', 'Mountain Bike', '适合山地和越野骑行的自行车'),
('公路车', 'Road Bike', '适合公路骑行的自行车'),
('城市车', 'City Bike', '适合城市通勤的自行车'),
('折叠车', 'Folding Bike', '可折叠便携的自行车'),
('电动车', 'Electric Bike', '电动助力自行车'),
('头盔', 'Helmet', '骑行安全头盔'),
('骑行服', 'Cycling Clothing', '专业骑行服装'),
('配件', 'Accessories', '各种骑行配件');