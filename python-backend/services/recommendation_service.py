import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from loguru import logger
from collections import defaultdict, Counter
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import math

class RecommendationService:
    """智能推荐服务类"""
    
    def __init__(self):
        self.recommendation_cache = {}  # 推荐结果缓存
        self.cache_timeout = 1800  # 缓存超时时间（秒）
        
        # 推荐权重配置
        self.weights = {
            'content_similarity': 0.3,  # 内容相似度
            'price_similarity': 0.2,    # 价格相似度
            'category_match': 0.2,      # 分类匹配
            'popularity': 0.15,         # 热门程度
            'rating': 0.15             # 评分
        }
        
        # 价格相似度阈值
        self.price_similarity_threshold = 0.5
        
        # TF-IDF向量化器
        self.tfidf_vectorizer = None
        self.content_matrix = None
        
    def get_equipment_recommendations(self, equipment_id: int, limit: int = 10) -> List[Dict]:
        """获取装备推荐"""
        try:
            from app import db, Equipment, EquipmentPrice
            
            # 检查缓存
            cache_key = f"equipment_{equipment_id}_{limit}"
            if self._is_cache_valid(cache_key):
                return self.recommendation_cache[cache_key]['data']
            
            # 获取目标装备信息
            target_equipment = Equipment.query.get(equipment_id)
            if not target_equipment:
                return []
            
            # 获取所有装备数据
            all_equipment = Equipment.query.filter(
                Equipment.id != equipment_id
            ).all()
            
            if not all_equipment:
                return []
            
            # 计算推荐分数
            recommendations = self._calculate_recommendation_scores(
                target_equipment, all_equipment
            )
            
            # 排序并限制数量
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            recommendations = recommendations[:limit]
            
            # 缓存结果
            self.recommendation_cache[cache_key] = {
                'data': recommendations,
                'timestamp': datetime.now()
            }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"获取装备推荐失败: {str(e)}")
            return []
    
    def get_category_recommendations(self, category: str, limit: int = 20) -> List[Dict]:
        """获取分类推荐"""
        try:
            from app import db, Equipment, EquipmentPrice
            
            # 检查缓存
            cache_key = f"category_{category}_{limit}"
            if self._is_cache_valid(cache_key):
                return self.recommendation_cache[cache_key]['data']
            
            # 获取分类下的装备
            from app import EquipmentCategory
            category_obj = EquipmentCategory.query.filter_by(name=category).first()
            if category_obj:
                equipment_list = Equipment.query.filter(
                    Equipment.category_id == category_obj.id
                ).all()
            else:
                equipment_list = []
            
            if not equipment_list:
                return []
            
            # 计算推荐分数（基于热门度和评分）
            recommendations = []
            for equipment in equipment_list:
                score = self._calculate_popularity_score(equipment)
                
                recommendations.append({
                    'id': equipment.id,
                    'name': equipment.name,
                    'brand': equipment.brand,
                    'category': equipment.category,
                    'price': float(equipment.price),
                    'rating': equipment.rating,
                    'rating_count': equipment.rating_count,
                    'image_urls': equipment.image_urls,
                    'score': score,
                    'reason': '热门推荐'
                })
            
            # 排序并限制数量
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            recommendations = recommendations[:limit]
            
            # 缓存结果
            self.recommendation_cache[cache_key] = {
                'data': recommendations,
                'timestamp': datetime.now()
            }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"获取分类推荐失败: {str(e)}")
            return []
    
    def get_price_based_recommendations(self, min_price: float, max_price: float, 
                                      category: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """基于价格范围的推荐"""
        try:
            from app import db, Equipment
            
            # 构建查询
            query = Equipment.query.filter(
                Equipment.price >= min_price,
                Equipment.price <= max_price
            )
            
            if category:
                from app import EquipmentCategory
                category_obj = EquipmentCategory.query.filter_by(name=category).first()
                if category_obj:
                    query = query.filter(Equipment.category_id == category_obj.id)
            
            equipment_list = query.all()
            
            if not equipment_list:
                return []
            
            # 计算推荐分数
            recommendations = []
            for equipment in equipment_list:
                # 价格位置分数（中等价位得分更高）
                price_position = (equipment.price - min_price) / (max_price - min_price)
                price_score = 1 - abs(price_position - 0.5) * 2  # 中间价位得分最高
                
                # 综合分数
                popularity_score = self._calculate_popularity_score(equipment)
                total_score = price_score * 0.4 + popularity_score * 0.6
                
                recommendations.append({
                    'id': equipment.id,
                    'name': equipment.name,
                    'brand': equipment.brand,
                    'category': equipment.category,
                    'price': float(equipment.price),
                    'rating': equipment.rating,
                    'rating_count': equipment.rating_count,
                    'image_urls': equipment.image_urls,
                    'score': total_score,
                    'reason': f'价格区间推荐 (¥{min_price}-¥{max_price})'
                })
            
            # 排序并限制数量
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            return recommendations[:limit]
            
        except Exception as e:
            logger.error(f"获取价格推荐失败: {str(e)}")
            return []
    
    def get_trending_recommendations(self, days: int = 7, limit: int = 20) -> List[Dict]:
        """获取趋势推荐（最近热门）"""
        try:
            from app import db, Equipment, EquipmentPrice
            
            # 检查缓存
            cache_key = f"trending_{days}_{limit}"
            if self._is_cache_valid(cache_key):
                return self.recommendation_cache[cache_key]['data']
            
            # 获取最近的价格记录（表示关注度）
            start_date = datetime.now() - timedelta(days=days)
            
            # 统计最近的价格记录数量
            price_stats = db.session.query(
                EquipmentPrice.equipment_id,
                db.func.count(EquipmentPrice.id).label('price_records'),
                db.func.avg(EquipmentPrice.price).label('avg_price')
            ).filter(
                EquipmentPrice.recorded_at >= start_date
            ).group_by(
                EquipmentPrice.equipment_id
            ).all()
            
            if not price_stats:
                return []
            
            # 获取装备详情
            equipment_ids = [stat.equipment_id for stat in price_stats]
            equipment_dict = {eq.id: eq for eq in Equipment.query.filter(
                Equipment.id.in_(equipment_ids)
            ).all()}
            
            # 计算趋势分数
            recommendations = []
            max_records = max(stat.price_records for stat in price_stats)
            
            for stat in price_stats:
                equipment = equipment_dict.get(stat.equipment_id)
                if not equipment:
                    continue
                
                # 趋势分数（基于最近的关注度）
                trend_score = stat.price_records / max_records
                
                # 综合分数
                popularity_score = self._calculate_popularity_score(equipment)
                total_score = trend_score * 0.6 + popularity_score * 0.4
                
                recommendations.append({
                    'id': equipment.id,
                    'name': equipment.name,
                    'brand': equipment.brand,
                    'category': equipment.category,
                    'price': float(equipment.price),
                    'rating': equipment.rating,
                    'rating_count': equipment.rating_count,
                    'image_urls': equipment.image_urls,
                    'score': total_score,
                    'trend_score': trend_score,
                    'price_records': stat.price_records,
                    'reason': f'最近{days}天热门'
                })
            
            # 排序并限制数量
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            recommendations = recommendations[:limit]
            
            # 缓存结果
            self.recommendation_cache[cache_key] = {
                'data': recommendations,
                'timestamp': datetime.now()
            }
            
            return recommendations
            
        except Exception as e:
            logger.error(f"获取趋势推荐失败: {str(e)}")
            return []
    
    def get_similar_equipment(self, equipment_id: int, limit: int = 10) -> List[Dict]:
        """获取相似装备"""
        try:
            from app import db, Equipment
            
            # 获取目标装备
            target_equipment = Equipment.query.get(equipment_id)
            if not target_equipment:
                return []
            
            # 获取同分类的装备
            similar_equipment = Equipment.query.filter(
                Equipment.category_id == target_equipment.category_id,
                Equipment.id != equipment_id
            ).all()
            
            if not similar_equipment:
                return []
            
            # 计算相似度
            similarities = []
            for equipment in similar_equipment:
                similarity_score = self._calculate_equipment_similarity(
                    target_equipment, equipment
                )
                
                similarities.append({
                    'id': equipment.id,
                    'name': equipment.name,
                    'brand': equipment.brand,
                    'category': equipment.category,
                    'price': float(equipment.price),
                    'rating': equipment.rating,
                    'rating_count': equipment.rating_count,
                    'image_urls': equipment.image_urls,
                    'similarity_score': similarity_score,
                    'reason': '相似产品'
                })
            
            # 排序并限制数量
            similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
            return similarities[:limit]
            
        except Exception as e:
            logger.error(f"获取相似装备失败: {str(e)}")
            return []
    
    def _calculate_recommendation_scores(self, target_equipment, all_equipment) -> List[Dict]:
        """计算推荐分数"""
        recommendations = []
        
        for equipment in all_equipment:
            # 内容相似度
            content_sim = self._calculate_content_similarity(target_equipment, equipment)
            
            # 价格相似度
            price_sim = self._calculate_price_similarity(target_equipment, equipment)
            
            # 分类匹配
            category_match = 1.0 if target_equipment.category == equipment.category else 0.3
            
            # 热门程度
            popularity = self._calculate_popularity_score(equipment)
            
            # 评分
            rating_score = equipment.rating / 5.0 if equipment.rating else 0.5
            
            # 综合分数
            total_score = (
                content_sim * self.weights['content_similarity'] +
                price_sim * self.weights['price_similarity'] +
                category_match * self.weights['category_match'] +
                popularity * self.weights['popularity'] +
                rating_score * self.weights['rating']
            )
            
            # 确定推荐理由
            reason = self._determine_recommendation_reason(
                content_sim, price_sim, category_match, popularity, rating_score
            )
            
            recommendations.append({
                'id': equipment.id,
                'name': equipment.name,
                'brand': equipment.brand,
                'category': equipment.category,
                'price': float(equipment.price),
                'rating': equipment.rating,
                'rating_count': equipment.rating_count,
                'image_urls': equipment.image_urls,
                'score': total_score,
                'reason': reason,
                'similarity_details': {
                    'content': content_sim,
                    'price': price_sim,
                    'category': category_match,
                    'popularity': popularity,
                    'rating': rating_score
                }
            })
        
        return recommendations
    
    def _calculate_content_similarity(self, equipment1, equipment2) -> float:
        """计算内容相似度"""
        try:
            # 组合文本内容
            text1 = f"{equipment1.name} {equipment1.brand} {equipment1.description or ''}"
            text2 = f"{equipment2.name} {equipment2.brand} {equipment2.description or ''}"
            
            # 使用TF-IDF计算相似度
            vectorizer = TfidfVectorizer(stop_words=None, max_features=1000)
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            
            # 计算余弦相似度
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"计算内容相似度失败: {str(e)}")
            return 0.0
    
    def _calculate_price_similarity(self, equipment1, equipment2) -> float:
        """计算价格相似度"""
        try:
            price1 = float(equipment1.price)
            price2 = float(equipment2.price)
            
            if price1 == 0 or price2 == 0:
                return 0.0
            
            # 计算价格差异比例
            price_diff = abs(price1 - price2) / max(price1, price2)
            
            # 转换为相似度（差异越小，相似度越高）
            similarity = max(0, 1 - price_diff)
            
            return similarity
            
        except Exception as e:
            logger.error(f"计算价格相似度失败: {str(e)}")
            return 0.0
    
    def _calculate_popularity_score(self, equipment) -> float:
        """计算热门程度分数"""
        try:
            # 基于评分数量和评分值
            rating_count = equipment.rating_count or 0
            rating = equipment.rating or 0
            
            # 对数缩放评分数量
            log_count = math.log(rating_count + 1) / math.log(1000)  # 假设1000为高评分数量
            log_count = min(1.0, log_count)
            
            # 评分标准化
            rating_norm = rating / 5.0 if rating > 0 else 0.5
            
            # 综合分数
            popularity = log_count * 0.6 + rating_norm * 0.4
            
            return popularity
            
        except Exception as e:
            logger.error(f"计算热门程度失败: {str(e)}")
            return 0.0
    
    def _calculate_equipment_similarity(self, equipment1, equipment2) -> float:
        """计算装备相似度"""
        # 内容相似度
        content_sim = self._calculate_content_similarity(equipment1, equipment2)
        
        # 价格相似度
        price_sim = self._calculate_price_similarity(equipment1, equipment2)
        
        # 品牌匹配
        brand_match = 1.0 if equipment1.brand == equipment2.brand else 0.0
        
        # 综合相似度
        similarity = content_sim * 0.5 + price_sim * 0.3 + brand_match * 0.2
        
        return similarity
    
    def _determine_recommendation_reason(self, content_sim, price_sim, category_match, 
                                       popularity, rating_score) -> str:
        """确定推荐理由"""
        scores = {
            '内容相似': content_sim,
            '价格相近': price_sim,
            '同类产品': category_match,
            '热门产品': popularity,
            '高评分': rating_score
        }
        
        # 找出最高分的理由
        max_reason = max(scores.items(), key=lambda x: x[1])
        
        return max_reason[0]
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """检查缓存是否有效"""
        if cache_key not in self.recommendation_cache:
            return False
        
        cache_time = self.recommendation_cache[cache_key]['timestamp']
        return (datetime.now() - cache_time).total_seconds() < self.cache_timeout
    
    def clear_cache(self):
        """清空缓存"""
        self.recommendation_cache.clear()
        logger.info("推荐缓存已清空")
    
    def get_recommendation_stats(self) -> Dict:
        """获取推荐统计信息"""
        try:
            from app import db, Equipment
            
            # 统计各分类的装备数量
            from app import EquipmentCategory
            category_stats = db.session.query(
                EquipmentCategory.name.label('category'),
                db.func.count(Equipment.id).label('count'),
                db.func.avg(Equipment.price).label('avg_price'),
                db.func.avg(Equipment.rating).label('avg_rating')
            ).join(
                EquipmentCategory, Equipment.category_id == EquipmentCategory.id
            ).group_by(EquipmentCategory.name).all()
            
            stats = {
                'total_equipment': Equipment.query.count(),
                'cache_size': len(self.recommendation_cache),
                'categories': []
            }
            
            for stat in category_stats:
                stats['categories'].append({
                    'category': stat.category,
                    'count': stat.count,
                    'avg_price': round(float(stat.avg_price or 0), 2),
                    'avg_rating': round(float(stat.avg_rating or 0), 2)
                })
            
            return stats
            
        except Exception as e:
            logger.error(f"获取推荐统计失败: {str(e)}")
            return {'error': str(e)}