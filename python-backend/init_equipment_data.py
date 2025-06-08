#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
装备数据初始化脚本
用于为装备推荐系统添加测试数据
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from datetime import datetime
from decimal import Decimal
from sqlalchemy import text
import json

def init_equipment_data():
    """初始化装备数据"""
    with app.app_context():
        try:
            # 简单的装备数据
            equipment_data = [
                ('GIRO Aether MIPS 头盔', 'GIRO', 'Aether MIPS', '头盔', '轻量化高端公路车头盔，配备MIPS技术', 4.8),
                ('Pearl Izumi Elite 骑行服', 'Pearl Izumi', 'Elite', '骑行服', '专业级骑行服，透气排汗', 4.6),
                ('Shimano SPD-SL 锁鞋', 'Shimano', 'SPD-SL', '骑行鞋', '公路车专用锁鞋，高效传动', 4.7)
            ]
            
            # 使用原始SQL插入装备数据
            for name, brand, model, category, description, rating in equipment_data:
                # 检查装备是否已存在
                existing = db.session.execute(
                    text("SELECT id FROM equipment WHERE name = :name"),
                    {'name': name}
                ).fetchone()
                
                if not existing:
                    # 插入装备数据
                    db.session.execute(
                        text("""
                        INSERT INTO equipment (
                            name, brand, model, category, description, rating
                        ) VALUES (:name, :brand, :model, :category, :description, :rating)
                        """),
                        {
                            'name': name,
                            'brand': brand, 
                            'model': model,
                            'category': category,
                            'description': description,
                            'rating': rating
                        }
                    )
                    print(f"已插入装备: {name}")
                else:
                    print(f"装备已存在: {name}")
            
            # 提交事务
            db.session.commit()
            print("装备数据初始化完成！")
            
        except Exception as e:
            db.session.rollback()
            print(f"初始化失败: {e}")
            raise

if __name__ == '__main__':
    init_equipment_data()




if __name__ == '__main__':
    init_equipment_data()