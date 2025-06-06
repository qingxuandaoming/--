from sqlalchemy import and_, or_, desc, func
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from models.equipment import Equipment, EquipmentCategory, EquipmentPrice, EquipmentReview
from app import db
from loguru import logger
import re
from collections import defaultdict

class EquipmentService:
    """装备服务类"""
    
    def __init__(self):
        pass
    
    def get_all_categories(self):
        """获取所有装备分类"""
        try:
            # 获取顶级分类（没有父分类的）
            top_categories = EquipmentCategory.query.filter(
                EquipmentCategory.parent_id.is_(None),
                EquipmentCategory.is_active == True
            ).order_by(EquipmentCategory.sort_order).all()
            
            return [category.to_dict() for category in top_categories]
        
        except Exception as e:
            logger.error(f"获取装备分类失败: {str(e)}")
            raise
    
    def search_equipment(self, keyword='', category_id=None, min_price=None, 
                        max_price=None, platform='', page=1, per_page=20):
        """搜索装备"""
        try:
            query = Equipment.query.filter(Equipment.is_active == True)
            
            # 关键词搜索
            if keyword:
                keyword_filter = or_(
                    Equipment.name.contains(keyword),
                    Equipment.brand.contains(keyword),
                    Equipment.description.contains(keyword)
                )
                query = query.filter(keyword_filter)
            
            # 分类筛选
            if category_id:
                query = query.filter(Equipment.category_id == category_id)
            
            # 价格筛选（基于最新价格）
            if min_price is not None or max_price is not None:
                # 子查询获取每个装备的最新价格
                latest_price_subquery = db.session.query(
                    EquipmentPrice.equipment_id,
                    func.max(EquipmentPrice.created_at).label('latest_time')
                ).group_by(EquipmentPrice.equipment_id).subquery()
                
                latest_prices = db.session.query(EquipmentPrice).join(
                    latest_price_subquery,
                    and_(
                        EquipmentPrice.equipment_id == latest_price_subquery.c.equipment_id,
                        EquipmentPrice.created_at == latest_price_subquery.c.latest_time
                    )
                ).subquery()
                
                query = query.join(latest_prices, Equipment.id == latest_prices.c.equipment_id)
                
                if min_price is not None:
                    query = query.filter(latest_prices.c.price >= min_price)
                if max_price is not None:
                    query = query.filter(latest_prices.c.price <= max_price)
            
            # 平台筛选
            if platform:
                equipment_ids_with_platform = db.session.query(
                    EquipmentPrice.equipment_id
                ).filter(EquipmentPrice.platform == platform).distinct().subquery()
                
                query = query.join(
                    equipment_ids_with_platform,
                    Equipment.id == equipment_ids_with_platform.c.equipment_id
                )
            
            # 排序：按评分和评价数量排序
            query = query.order_by(
                desc(Equipment.avg_rating),
                desc(Equipment.review_count),
                desc(Equipment.created_at)
            )
            
            # 分页
            total = query.count()
            equipment_list = query.offset((page - 1) * per_page).limit(per_page).all()
            
            # 获取装备的最新价格信息
            equipment_data = []
            for equipment in equipment_list:
                equipment_dict = equipment.to_dict()
                
                # 获取最新价格
                latest_prices = self.get_latest_prices(equipment.id)
                equipment_dict['latest_prices'] = latest_prices
                
                # 获取价格范围
                price_range = self.get_price_range(equipment.id)
                equipment_dict['price_range'] = price_range
                
                equipment_data.append(equipment_dict)
            
            return {
                'items': equipment_data,
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': (total + per_page - 1) // per_page
            }
        
        except Exception as e:
            logger.error(f"搜索装备失败: {str(e)}")
            raise
    
    def get_latest_prices(self, equipment_id, limit=5):
        """获取装备的最新价格"""
        try:
            prices = EquipmentPrice.query.filter(
                EquipmentPrice.equipment_id == equipment_id,
                EquipmentPrice.is_available == True
            ).order_by(desc(EquipmentPrice.created_at)).limit(limit).all()
            
            return [price.to_dict() for price in prices]
        
        except Exception as e:
            logger.error(f"获取最新价格失败: {str(e)}")
            return []
    
    def get_price_range(self, equipment_id):
        """获取装备的价格范围"""
        try:
            # 获取最近30天的价格数据
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            price_stats = db.session.query(
                func.min(EquipmentPrice.price).label('min_price'),
                func.max(EquipmentPrice.price).label('max_price'),
                func.avg(EquipmentPrice.price).label('avg_price')
            ).filter(
                EquipmentPrice.equipment_id == equipment_id,
                EquipmentPrice.created_at >= thirty_days_ago,
                EquipmentPrice.is_available == True
            ).first()
            
            if price_stats and price_stats.min_price:
                return {
                    'min_price': float(price_stats.min_price),
                    'max_price': float(price_stats.max_price),
                    'avg_price': float(price_stats.avg_price)
                }
            
            return None
        
        except Exception as e:
            logger.error(f"获取价格范围失败: {str(e)}")
            return None
    
    def get_price_history(self, equipment_id, days=30):
        """获取装备价格历史"""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            prices = EquipmentPrice.query.filter(
                EquipmentPrice.equipment_id == equipment_id,
                EquipmentPrice.created_at >= start_date
            ).order_by(EquipmentPrice.created_at).all()
            
            # 按平台分组
            platform_prices = defaultdict(list)
            for price in prices:
                platform_prices[price.platform].append(price.to_dict())
            
            # 计算价格趋势
            price_trend = self._calculate_price_trend(prices)
            
            return {
                'platform_prices': dict(platform_prices),
                'price_trend': price_trend,
                'total_records': len(prices)
            }
        
        except Exception as e:
            logger.error(f"获取价格历史失败: {str(e)}")
            raise
    
    def _calculate_price_trend(self, prices):
        """计算价格趋势"""
        if len(prices) < 2:
            return {'trend': 'stable', 'change_percent': 0}
        
        # 按时间排序
        sorted_prices = sorted(prices, key=lambda x: x.created_at)
        
        # 计算最近价格变化
        recent_prices = sorted_prices[-7:]  # 最近7个价格点
        if len(recent_prices) < 2:
            return {'trend': 'stable', 'change_percent': 0}
        
        first_price = float(recent_prices[0].price)
        last_price = float(recent_prices[-1].price)
        
        if first_price == 0:
            return {'trend': 'stable', 'change_percent': 0}
        
        change_percent = ((last_price - first_price) / first_price) * 100
        
        if change_percent > 5:
            trend = 'rising'
        elif change_percent < -5:
            trend = 'falling'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'change_percent': round(change_percent, 2),
            'first_price': first_price,
            'last_price': last_price
        }
    
    def get_recommendations(self, equipment_id, limit=10):
        """获取装备推荐"""
        try:
            # 获取当前装备信息
            current_equipment = Equipment.query.get(equipment_id)
            if not current_equipment:
                raise ValueError(f"装备 {equipment_id} 不存在")
            
            # 基于分类的推荐
            category_recommendations = self._get_category_recommendations(
                current_equipment, limit // 2
            )
            
            # 基于品牌的推荐
            brand_recommendations = self._get_brand_recommendations(
                current_equipment, limit // 2
            )
            
            # 合并推荐结果，去重
            all_recommendations = category_recommendations + brand_recommendations
            seen_ids = set()
            unique_recommendations = []
            
            for rec in all_recommendations:
                if rec['id'] not in seen_ids and rec['id'] != equipment_id:
                    seen_ids.add(rec['id'])
                    unique_recommendations.append(rec)
                    if len(unique_recommendations) >= limit:
                        break
            
            return unique_recommendations
        
        except Exception as e:
            logger.error(f"获取推荐失败: {str(e)}")
            raise
    
    def _get_category_recommendations(self, equipment, limit):
        """基于分类的推荐"""
        recommendations = Equipment.query.filter(
            Equipment.category_id == equipment.category_id,
            Equipment.id != equipment.id,
            Equipment.is_active == True
        ).order_by(
            desc(Equipment.avg_rating),
            desc(Equipment.review_count)
        ).limit(limit).all()
        
        result = []
        for rec in recommendations:
            rec_dict = rec.to_dict()
            rec_dict['recommendation_reason'] = '同类商品'
            rec_dict['latest_prices'] = self.get_latest_prices(rec.id, 3)
            result.append(rec_dict)
        
        return result
    
    def _get_brand_recommendations(self, equipment, limit):
        """基于品牌的推荐"""
        if not equipment.brand:
            return []
        
        recommendations = Equipment.query.filter(
            Equipment.brand == equipment.brand,
            Equipment.id != equipment.id,
            Equipment.is_active == True
        ).order_by(
            desc(Equipment.avg_rating),
            desc(Equipment.review_count)
        ).limit(limit).all()
        
        result = []
        for rec in recommendations:
            rec_dict = rec.to_dict()
            rec_dict['recommendation_reason'] = '同品牌商品'
            rec_dict['latest_prices'] = self.get_latest_prices(rec.id, 3)
            result.append(rec_dict)
        
        return result
    
    def get_equipment_detail(self, equipment_id):
        """获取装备详情"""
        try:
            equipment = Equipment.query.get(equipment_id)
            if not equipment:
                raise ValueError(f"装备 {equipment_id} 不存在")
            
            equipment_dict = equipment.to_dict(include_prices=True, include_reviews=True)
            
            # 获取价格历史
            price_history = self.get_price_history(equipment_id, 90)
            equipment_dict['price_history'] = price_history
            
            # 获取推荐商品
            recommendations = self.get_recommendations(equipment_id, 6)
            equipment_dict['recommendations'] = recommendations
            
            return equipment_dict
        
        except Exception as e:
            logger.error(f"获取装备详情失败: {str(e)}")
            raise
    
    def get_popular_equipment(self, category_id=None, limit=20):
        """获取热门装备"""
        try:
            query = Equipment.query.filter(Equipment.is_active == True)
            
            if category_id:
                query = query.filter(Equipment.category_id == category_id)
            
            # 按评分和评价数量排序
            equipment_list = query.order_by(
                desc(Equipment.avg_rating),
                desc(Equipment.review_count)
            ).limit(limit).all()
            
            result = []
            for equipment in equipment_list:
                equipment_dict = equipment.to_dict()
                equipment_dict['latest_prices'] = self.get_latest_prices(equipment.id, 3)
                result.append(equipment_dict)
            
            return result
        
        except Exception as e:
            logger.error(f"获取热门装备失败: {str(e)}")
            raise
    
    def get_price_alerts(self, user_id=None):
        """获取价格提醒（预留接口）"""
        # 这里可以实现价格提醒功能
        # 比如用户设置某个商品的目标价格，当价格低于目标价格时发送提醒
        pass
    
    def add_equipment_category(self, name, name_en, description=None, parent_id=None):
        """添加装备分类"""
        try:
            category = EquipmentCategory(
                name=name,
                name_en=name_en,
                description=description,
                parent_id=parent_id
            )
            
            db.session.add(category)
            db.session.commit()
            
            return category.to_dict()
        
        except Exception as e:
            logger.error(f"添加装备分类失败: {str(e)}")
            db.session.rollback()
            raise
    
    def update_equipment_rating(self, equipment_id):
        """更新装备评分"""
        try:
            # 计算平均评分和评价数量
            rating_stats = db.session.query(
                func.avg(EquipmentReview.rating).label('avg_rating'),
                func.count(EquipmentReview.id).label('review_count')
            ).filter(EquipmentReview.equipment_id == equipment_id).first()
            
            equipment = Equipment.query.get(equipment_id)
            if equipment and rating_stats:
                equipment.avg_rating = float(rating_stats.avg_rating) if rating_stats.avg_rating else 0.0
                equipment.review_count = rating_stats.review_count or 0
                
                db.session.commit()
                
                logger.info(f"更新装备 {equipment_id} 评分: {equipment.avg_rating}")
        
        except Exception as e:
            logger.error(f"更新装备评分失败: {str(e)}")
            db.session.rollback()