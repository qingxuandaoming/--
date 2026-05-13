-- 灵境行者 - 测试数据脚本
-- 创建时间：2025年1月
-- 用途：为系统添加丰富的测试数据

USE ljxz;

-- ============================================
-- 添加更多测试用户
-- ============================================

INSERT INTO `users` (`email`, `username`, `password_hash`, `nickname`, `phone`, `status`) VALUES
('cyclist1@ljxz.com', 'cyclist1', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', '骑行达人小王', '13811111111', 1),
('cyclist2@ljxz.com', 'cyclist2', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', '山地车爱好者', '13822222222', 1),
('cyclist3@ljxz.com', 'cyclist3', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', '公路车女神', '13833333333', 1),
('cyclist4@ljxz.com', 'cyclist4', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', '周末骑士', '13844444444', 1),
('cyclist5@ljxz.com', 'cyclist5', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', '城市通勤族', '13855555555', 1);

-- ============================================
-- 添加更多骑行路线
-- ============================================

INSERT INTO `cycling_routes` (`user_id`, `name`, `description`, `start_latitude`, `start_longitude`, `start_address`, `end_latitude`, `end_longitude`, `end_address`, `difficulty`, `estimated_time`, `distance`, `elevation_gain`, `city`, `province`, `tags`) VALUES
-- 杭州地区路线
(4, '灵隐寺祈福骑行', '从市区骑行到灵隐寺，沿途欣赏佛教文化，适合文化骑行', 30.2467, 120.1234, '杭州市西湖区文二路', 30.2398, 120.1009, '杭州市西湖区灵隐寺', 'MEDIUM', 105, 16.8, 180, '杭州', '浙江', '["文化", "佛教", "爬坡"]'),
(5, '九溪十八涧探秘', '九溪烟树到十八涧，山水相依的自然骑行路线', 30.2156, 120.1234, '杭州市西湖区九溪烟树', 30.1987, 120.1156, '杭州市西湖区十八涧', 'HARD', 150, 19.5, 420, '杭州', '浙江', '["自然", "山水", "挑战"]'),
(6, '良渚文化村休闲游', '良渚文化村内的休闲骑行，适合家庭出游', 30.3789, 120.0234, '余杭区良渚文化村', 30.3856, 120.0345, '余杭区良渚博物院', 'EASY', 60, 8.9, 25, '杭州', '浙江', '["休闲", "文化", "家庭"]'),
(7, '萧山湘湖环湖', '萧山湘湖风景区环湖骑行，风景秀丽', 30.1567, 120.2789, '萧山区湘湖景区东门', 30.1567, 120.2789, '萧山区湘湖景区东门', 'EASY', 80, 11.2, 35, '杭州', '浙江', '["环湖", "风景", "轻松"]'),
(8, '富阳新沙岛骑行', '富阳新沙岛田园风光骑行，体验乡村生活', 30.0456, 119.9123, '富阳区新沙岛码头', 30.0523, 119.9234, '富阳区新沙岛农庄', 'EASY', 90, 13.6, 15, '杭州', '浙江', '["田园", "乡村", "平坦"]'),

-- 其他城市路线
(4, '上海外滩夜骑', '上海外滩到陆家嘴的夜间骑行，欣赏都市夜景', 31.2304, 121.4737, '上海市黄浦区外滩', 31.2397, 121.4994, '上海市浦东新区陆家嘴', 'EASY', 45, 6.8, 10, '上海', '上海', '["夜骑", "都市", "夜景"]'),
(5, '苏州古城墙骑行', '沿苏州古城墙骑行，感受古城韵味', 31.2989, 120.6189, '苏州市姑苏区平江路', 31.3156, 120.6234, '苏州市姑苏区山塘街', 'EASY', 75, 12.3, 20, '苏州', '江苏', '["古城", "文化", "历史"]'),
(6, '南京紫金山挑战', '南京紫金山登山骑行，挑战性较强', 32.0603, 118.8067, '南京市玄武区紫金山索道', 32.0689, 118.8234, '南京市玄武区紫金山天文台', 'HARD', 120, 15.8, 380, '南京', '江苏', '["登山", "挑战", "天文"]'),
(7, '无锡太湖环湖', '无锡太湖风景区环湖骑行，湖光山色', 31.4689, 120.2567, '无锡市滨湖区太湖广场', 31.4689, 120.2567, '无锡市滨湖区太湖广场', 'MEDIUM', 180, 28.9, 120, '无锡', '江苏', '["环湖", "太湖", "风景"]'),
(8, '绍兴古镇串联', '绍兴各古镇之间的骑行路线，体验水乡文化', 30.0123, 120.5789, '绍兴市越城区鲁迅故里', 29.9876, 120.6123, '绍兴市柯桥区安昌古镇', 'MEDIUM', 135, 22.4, 85, '绍兴', '浙江', '["古镇", "水乡", "文化"]');

-- ============================================
-- 添加更多设备数据
-- ============================================

INSERT INTO `equipment` (`name`, `category_id`, `brand`, `model`, `price`, `original_price`, `description`, `specifications`, `images`, `availability`, `source`, `source_url`) VALUES
-- 更多自行车
('Trek Domane AL 2 公路车', 8, 'Trek', 'Domane AL 2', 4999.00, 5499.00, '入门级公路车，舒适几何设计', '{"frame": "铝合金车架", "wheelSize": "700C", "gears": "16速", "weight": "10.2kg", "brakes": "机械碟刹"}', '["https://example.com/trek1.jpg"]', 1, '京东', 'https://item.jd.com/trek1.html'),
('大行 K3 折叠车', 9, '大行', 'K3', 1299.00, 1499.00, '经典折叠车，便携实用', '{"frame": "铝合金车架", "wheelSize": "14寸", "gears": "3速", "weight": "11.8kg", "foldSize": "80x34x64cm"}', '["https://example.com/dahon1.jpg"]', 1, '天猫', 'https://detail.tmall.com/dahon1.html'),
('小牛 NGT 电动车', 10, '小牛', 'NGT', 7999.00, 8999.00, '智能电动自行车，续航持久', '{"motor": "中置电机", "battery": "48V 20Ah", "range": "100km", "weight": "22.5kg", "maxSpeed": "25km/h"}', '["https://example.com/niu1.jpg"]', 1, '官网', 'https://niu.com/ngt.html'),

-- 骑行服装
('Rapha Core Jersey 骑行上衣', 12, 'Rapha', 'Core Jersey', 899.00, 999.00, '专业骑行上衣，透气排汗', '{"material": "聚酯纤维", "fit": "修身剪裁", "pockets": "3个后袋", "sizes": ["S", "M", "L", "XL"]}', '["https://example.com/rapha1.jpg"]', 1, '天猫', 'https://detail.tmall.com/rapha1.html'),
('Pearl Izumi 骑行短裤', 13, 'Pearl Izumi', 'Attack Short', 699.00, 799.00, '专业骑行短裤，舒适坐垫', '{"material": "尼龙弹性面料", "pad": "3D立体坐垫", "length": "9寸", "sizes": ["S", "M", "L", "XL"]}', '["https://example.com/pi1.jpg"]', 1, '京东', 'https://item.jd.com/pi1.html'),
('Giro DND 骑行手套', 14, 'Giro', 'DND Glove', 299.00, 349.00, '半指骑行手套，防滑耐磨', '{"material": "合成革", "padding": "掌部加厚", "closure": "魔术贴", "sizes": ["S", "M", "L", "XL"]}', '["https://example.com/giro_glove1.jpg"]', 1, '天猫', 'https://detail.tmall.com/giro_glove1.html'),

-- 更多头盔
('POC Ventral Air SPIN 头盔', 16, 'POC', 'Ventral Air SPIN', 1899.00, 2199.00, '专业公路车头盔，SPIN技术', '{"weight": "230g", "vents": "22个通风孔", "technology": "SPIN", "sizes": ["S", "M", "L"]}', '["https://example.com/poc1.jpg"]', 1, '京东', 'https://item.jd.com/poc1.html'),
('Bell Super Air R MIPS 头盔', 16, 'Bell', 'Super Air R MIPS', 1599.00, 1799.00, '山地车头盔，可拆卸下巴护具', '{"weight": "350g", "vents": "18个通风孔", "technology": "MIPS", "removable": "可拆卸下巴护具"}', '["https://example.com/bell1.jpg"]', 1, '天猫', 'https://detail.tmall.com/bell1.html'),

-- 骑行配件
('Lezyne Macro Drive 1300XL 车灯', 20, 'Lezyne', 'Macro Drive 1300XL', 899.00, 999.00, '高亮度前灯，USB充电', '{"brightness": "1300流明", "battery": "4400mAh", "runtime": "2-150小时", "waterproof": "IPX7"}', '["https://example.com/lezyne1.jpg"]', 1, '京东', 'https://item.jd.com/lezyne1.html'),
('Wahoo ELEMNT BOLT 码表', 21, 'Wahoo', 'ELEMNT BOLT', 1999.00, 2299.00, 'GPS骑行码表，空气动力学设计', '{"screen": "2.2寸单色屏", "battery": "15小时", "gps": "GPS+GLONASS+Galileo+QZSS", "sensors": "ANT+/蓝牙"}', '["https://example.com/wahoo1.jpg"]', 1, '天猫', 'https://detail.tmall.com/wahoo1.html'),
('Elite Vico Carbon 水壶架', 22, 'Elite', 'Vico Carbon', 299.00, 349.00, '碳纤维水壶架，轻量化', '{"material": "碳纤维", "weight": "18g", "compatibility": "标准水壶", "mounting": "标准螺丝固定"}', '["https://example.com/elite1.jpg"]', 1, '京东', 'https://item.jd.com/elite1.html'),
('Kryptonite New York Fahgettaboudit 车锁', 23, 'Kryptonite', 'New York Fahgettaboudit', 899.00, 1099.00, '最高安全级别U型锁', '{"material": "硬化钢", "thickness": "18mm", "size": "13x15cm", "security": "10/10级别"}', '["https://example.com/kryptonite1.jpg"]', 1, '天猫', 'https://detail.tmall.com/kryptonite1.html');

-- ============================================
-- 添加更多骑行记录
-- ============================================

INSERT INTO `cycling_records` (`user_id`, `route_id`, `start_latitude`, `start_longitude`, `end_latitude`, `end_longitude`, `total_distance`, `total_time`, `average_speed`, `max_speed`, `calories`, `elevation_gain`, `start_time`, `end_time`, `status`) VALUES
-- 用户4的骑行记录
(4, 6, 30.2467, 120.1234, 30.2398, 120.1009, 16.5, 6180, 9.6, 25.3, 680, 175, '2025-01-10 07:30:00', '2025-01-10 09:13:00', 'COMPLETED'),
(4, 1, 30.2741, 120.1551, 30.2441, 120.1351, 12.8, 4980, 9.3, 22.1, 450, 55, '2025-01-12 08:15:00', '2025-01-12 09:38:00', 'COMPLETED'),
(4, 11, 31.2304, 121.4737, 31.2397, 121.4994, 7.2, 1980, 13.1, 28.7, 280, 12, '2025-01-14 19:30:00', '2025-01-14 20:03:00', 'COMPLETED'),

-- 用户5的骑行记录
(5, 7, 30.2156, 120.1234, 30.1987, 120.1156, 19.8, 8760, 8.1, 31.5, 920, 435, '2025-01-11 06:45:00', '2025-01-11 09:11:00', 'COMPLETED'),
(5, 8, 30.3789, 120.0234, 30.3856, 120.0345, 9.1, 3420, 9.6, 18.9, 320, 28, '2025-01-13 10:00:00', '2025-01-13 10:57:00', 'COMPLETED'),
(5, 12, 31.2989, 120.6189, 31.3156, 120.6234, 12.6, 4500, 10.1, 24.6, 420, 22, '2025-01-15 14:30:00', '2025-01-15 15:45:00', 'COMPLETED'),

-- 用户6的骑行记录
(6, 9, 30.1567, 120.2789, 30.1567, 120.2789, 11.5, 4680, 8.8, 19.2, 380, 38, '2025-01-09 16:00:00', '2025-01-09 17:18:00', 'COMPLETED'),
(6, 13, 32.0603, 118.8067, 32.0689, 118.8234, 16.2, 7200, 8.1, 28.9, 780, 395, '2025-01-16 08:00:00', '2025-01-16 10:00:00', 'COMPLETED'),
(6, 2, 29.6050, 119.0350, 29.6050, 119.0350, 38.9, 9180, 15.2, 38.7, 1350, 325, '2025-01-17 06:30:00', '2025-01-17 09:03:00', 'COMPLETED'),

-- 用户7的骑行记录
(7, 10, 30.0456, 119.9123, 30.0523, 119.9234, 13.8, 5280, 9.4, 21.3, 480, 18, '2025-01-08 15:30:00', '2025-01-08 16:58:00', 'COMPLETED'),
(7, 14, 31.4689, 120.2567, 31.4689, 120.2567, 29.5, 10800, 9.8, 32.1, 1180, 125, '2025-01-18 07:00:00', '2025-01-18 10:00:00', 'COMPLETED'),

-- 用户8的骑行记录
(8, 15, 30.0123, 120.5789, 29.9876, 120.6123, 22.8, 8100, 10.1, 26.8, 820, 88, '2025-01-19 09:00:00', '2025-01-19 11:15:00', 'COMPLETED'),
(8, 3, 30.2467, 120.2103, 30.2890, 120.1552, 15.9, 4320, 13.2, 29.4, 520, 32, '2025-01-20 07:45:00', '2025-01-20 08:57:00', 'COMPLETED');

-- ============================================
-- 添加更多互动数据
-- ============================================

-- 更多路线点赞
INSERT INTO `route_likes` (`user_id`, `route_id`) VALUES
(4, 2), (4, 7), (4, 12), (4, 13),
(5, 3), (5, 6), (5, 8), (5, 14),
(6, 4), (6, 9), (6, 11), (6, 15),
(7, 5), (7, 10), (7, 1), (7, 6),
(8, 1), (8, 7), (8, 9), (8, 11);

-- 更多路线收藏
INSERT INTO `route_favorites` (`user_id`, `route_id`) VALUES
(4, 6), (4, 7), (4, 11), (4, 13),
(5, 8), (5, 12), (5, 14), (5, 2),
(6, 9), (6, 13), (6, 15), (6, 1),
(7, 10), (7, 14), (7, 3), (7, 6),
(8, 15), (8, 11), (8, 5), (8, 7);

-- 更多路线评分
INSERT INTO `route_ratings` (`user_id`, `route_id`, `rating`, `comment`) VALUES
(4, 6, 4, '灵隐寺的路线很有文化气息，就是爬坡有点累'),
(4, 11, 5, '上海外滩夜骑太棒了！夜景超美，强烈推荐'),
(5, 7, 5, '九溪十八涧真的很美，虽然有挑战但值得'),
(5, 8, 4, '良渚文化村很适合家庭骑行，路况很好'),
(6, 9, 4, '湘湖环湖路线不错，风景优美，难度适中'),
(6, 13, 3, '紫金山爬坡太累了，不过山顶风景还可以'),
(7, 10, 5, '新沙岛的田园风光太美了，很放松的路线'),
(7, 14, 4, '太湖环湖路线很长，需要体力，但风景绝佳'),
(8, 15, 4, '绍兴古镇串联很有意思，可以体验水乡文化'),
(8, 3, 5, '钱塘江沿岸骑行路线平坦好骑，江景很美');

-- 更多设备收藏
INSERT INTO `user_equipment_favorites` (`user_id`, `equipment_id`) VALUES
(4, 6), (4, 10), (4, 15), (4, 18),
(5, 7), (5, 11), (5, 16), (5, 19),
(6, 8), (6, 12), (6, 17), (6, 20),
(7, 9), (7, 13), (7, 14), (7, 21),
(8, 6), (8, 15), (8, 22), (8, 23);

-- 更多价格提醒
INSERT INTO `price_alerts` (`user_id`, `equipment_id`, `target_price`) VALUES
(4, 6, 4500.00), (4, 10, 7000.00), (4, 15, 800.00),
(5, 7, 1100.00), (5, 11, 850.00), (5, 16, 1600.00),
(6, 8, 1700.00), (6, 12, 650.00), (6, 17, 250.00),
(7, 9, 250.00), (7, 13, 600.00), (7, 21, 1800.00),
(8, 22, 250.00), (8, 23, 800.00);

-- 更多用户设备
INSERT INTO `user_devices` (`user_id`, `device_id`, `device_type`, `device_name`, `manufacturer`, `model`) VALUES
(4, 'WAHOO_BOLT_001', 'BIKE_COMPUTER', 'Wahoo ELEMNT BOLT', 'Wahoo', 'ELEMNT BOLT'),
(5, 'GARMIN_WATCH_001', 'HEART_RATE_MONITOR', 'Garmin Forerunner 945', 'Garmin', 'Forerunner 945'),
(6, 'STAGES_POWER_001', 'POWER_METER', 'Stages Power LR', 'Stages', 'Power LR'),
(7, 'TACX_TRAINER_001', 'SMART_TRAINER', 'Tacx Neo 2T', 'Tacx', 'Neo 2T'),
(8, 'ANDROID_APP_001', 'MOBILE_APP', 'Android 骑行应用', 'Google', 'Pixel 6');

-- ============================================
-- 添加反馈数据
-- ============================================

INSERT INTO `feedback` (`user_id`, `subject`, `message`, `contact_email`, `status`) VALUES
(4, '路线推荐功能建议', '希望能根据用户的骑行历史和偏好推荐合适的路线', 'cyclist1@ljxz.com', 'PENDING'),
(5, '设备价格提醒问题', '设置的价格提醒没有及时收到通知，希望能改进', 'cyclist2@ljxz.com', 'IN_PROGRESS'),
(6, '地图显示问题', '在某些地区地图显示不完整，影响路线规划', 'cyclist3@ljxz.com', 'RESOLVED'),
(7, '数据同步建议', '希望能支持更多品牌的骑行设备数据同步', 'cyclist4@ljxz.com', 'PENDING'),
(8, '社交功能建议', '建议增加骑友圈功能，可以和其他骑友交流', 'cyclist5@ljxz.com', 'PENDING');

-- ============================================
-- 添加爬虫任务数据
-- ============================================

INSERT INTO `crawler_tasks` (`task_id`, `task_type`, `sources`, `categories`, `status`, `progress`, `results`) VALUES
('TASK_20250120_001', 'FULL_CRAWL', '["京东", "天猫", "淘宝"]', '["自行车", "骑行配件"]', 'COMPLETED', '{"total": 1000, "completed": 1000, "failed": 0}', '{"new_products": 156, "updated_prices": 844, "total_time": "2h 15m"}'),
('TASK_20250120_002', 'PRICE_UPDATE', '["京东", "天猫"]', '["头盔", "车灯"]', 'COMPLETED', '{"total": 500, "completed": 500, "failed": 0}', '{"price_changes": 23, "total_time": "45m"}'),
('TASK_20250121_001', 'INCREMENTAL_CRAWL', '["京东"]', '["山地车", "公路车"]', 'RUNNING', '{"total": 300, "completed": 180, "failed": 2}', '{}'),
('TASK_20250121_002', 'FULL_CRAWL', '["官网"]', '["高端设备"]', 'PENDING', '{}', '{}');

-- ============================================
-- 更新统计数据
-- ============================================

-- 更新所有路线的点赞数和浏览数
UPDATE `cycling_routes` SET 
  `like_count` = (SELECT COUNT(*) FROM `route_likes` WHERE `route_id` = `cycling_routes`.`id`),
  `view_count` = `like_count` * 8 + FLOOR(RAND() * 50) + 20
WHERE `id` > 0;

-- 更新设备评分和评价数
UPDATE `equipment` SET 
  `rating` = 3.5 + (RAND() * 1.5),
  `review_count` = FLOOR(RAND() * 200) + 10,
  `sales_count` = FLOOR(RAND() * 500) + 50
WHERE `id` > 0;

-- 插入一些设备价格历史记录
INSERT INTO `equipment_price_history` (`equipment_id`, `price`, `original_price`, `discount`, `availability`, `stock`) 
SELECT 
  `id`,
  `price` + (RAND() * 200 - 100),
  `original_price`,
  `discount`,
  1,
  FLOOR(RAND() * 100) + 10
FROM `equipment` 
WHERE `id` <= 10;

COMMIT;

SELECT 'Test data insertion completed successfully!' as message;
SELECT 
  (SELECT COUNT(*) FROM users) as total_users,
  (SELECT COUNT(*) FROM cycling_routes) as total_routes,
  (SELECT COUNT(*) FROM cycling_records) as total_records,
  (SELECT COUNT(*) FROM equipment) as total_equipment,
  (SELECT COUNT(*) FROM route_likes) as total_likes,
  (SELECT COUNT(*) FROM route_favorites) as total_favorites;