-- 创建数据库
CREATE DATABASE IF NOT EXISTS ljxz CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE ljxz;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- 骑行路线表
CREATE TABLE IF NOT EXISTS cycling_routes (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    start_location VARCHAR(255) NOT NULL,
    end_location VARCHAR(255) NOT NULL,
    distance DECIMAL(8,2), -- 距离（公里）
    difficulty_level ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
    estimated_time INT, -- 预计时间（分钟）
    route_data JSON, -- 路线坐标数据
    elevation_gain INT, -- 爬升高度（米）
    created_by BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- 骑行记录表
CREATE TABLE IF NOT EXISTS cycling_records (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    route_id BIGINT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    actual_distance DECIMAL(8,2), -- 实际骑行距离
    actual_time INT, -- 实际骑行时间（分钟）
    average_speed DECIMAL(5,2), -- 平均速度（km/h）
    max_speed DECIMAL(5,2), -- 最高速度（km/h）
    calories_burned INT, -- 消耗卡路里
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (route_id) REFERENCES cycling_routes(id) ON DELETE SET NULL
);

-- 用户反馈表
CREATE TABLE IF NOT EXISTS feedback (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    contact_email VARCHAR(100),
    status ENUM('pending', 'in_progress', 'resolved', 'closed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 路线收藏表
CREATE TABLE IF NOT EXISTS route_favorites (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    route_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (route_id) REFERENCES cycling_routes(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_route (user_id, route_id)
);

-- 路线评分表
CREATE TABLE IF NOT EXISTS route_ratings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    route_id BIGINT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (route_id) REFERENCES cycling_routes(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_route_rating (user_id, route_id)
);

-- 创建索引以提高查询性能
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_routes_difficulty ON cycling_routes(difficulty_level);
CREATE INDEX idx_routes_distance ON cycling_routes(distance);
CREATE INDEX idx_records_user_id ON cycling_records(user_id);
CREATE INDEX idx_records_start_time ON cycling_records(start_time);
CREATE INDEX idx_feedback_status ON feedback(status);
CREATE INDEX idx_feedback_created_at ON feedback(created_at);

-- 插入示例数据
-- 插入管理员账户（密码：123456，已使用BCrypt加密）
INSERT INTO users (username, email, password_hash, full_name, is_active) VALUES
('admin', 'admin@ljxz.com', '$2a$10$N9qo8uLOickgx2ZMRZoMye.IjdJrjrdHxdF6ufHZ6jO0OMKaaezIm', '系统管理员', TRUE);

INSERT INTO cycling_routes (name, description, start_location, end_location, distance, difficulty_level, estimated_time, elevation_gain) VALUES
('城市环线', '适合初学者的城市骑行路线，路况良好，风景优美', '市中心广场', '滨江公园', 15.5, 'easy', 60, 50),
('山地挑战', '具有挑战性的山地骑行路线，适合有经验的骑手', '山脚停车场', '山顶观景台', 25.8, 'hard', 120, 800),
('郊外休闲', '轻松的郊外骑行路线，适合周末休闲', '郊外入口', '湖边小镇', 20.2, 'medium', 90, 200);

COMMIT;