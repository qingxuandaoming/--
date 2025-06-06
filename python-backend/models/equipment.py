from datetime import datetime
from sqlalchemy import Index, DECIMAL
from decimal import Decimal
from flask_sqlalchemy import SQLAlchemy

# 延迟导入db实例
def get_db():
    from app import db
    return db

# 创建基类
class BaseModel:
    @property
    def db(self):
        return get_db()

class EquipmentCategory(BaseModel):
    """装备分类表"""
    def __init__(self):
        # 动态创建模型类
        db = get_db()
        
        class _EquipmentCategory(db.Model):
            __tablename__ = 'equipment_categories'
            
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(50), nullable=False, unique=True, comment='分类名称')
            name_en = db.Column(db.String(50), nullable=False, comment='英文名称')
            description = db.Column(db.Text, comment='分类描述')
            parent_id = db.Column(db.Integer, db.ForeignKey('equipment_categories.id'), comment='父分类ID')
            sort_order = db.Column(db.Integer, default=0, comment='排序')
            is_active = db.Column(db.Boolean, default=True, comment='是否启用')
            created_at = db.Column(db.DateTime, default=datetime.utcnow)
            updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
            
            # 关系
            children = db.relationship('EquipmentCategory', backref=db.backref('parent', remote_side=[id]))
            equipment = db.relationship('Equipment', backref='category', lazy='dynamic')
            
            def to_dict(self):
                return {
                    'id': self.id,
                    'name': self.name,
                    'name_en': self.name_en,
                    'description': self.description,
                    'parent_id': self.parent_id,
                    'sort_order': self.sort_order,
                    'is_active': self.is_active,
                    'children': [child.to_dict() for child in self.children if child.is_active]
                }
        
        self.__class__ = _EquipmentCategory

# 简化方法：直接在模块级别创建模型
# 这需要在app.py中正确设置导入顺序

# 让我们使用更简单的方法
from flask import current_app

def create_models(db):
    """创建所有模型类"""
    
    class EquipmentCategory(db.Model):
        """装备分类表"""
        __tablename__ = 'equipment_categories'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False, unique=True, comment='分类名称')
        name_en = db.Column(db.String(50), nullable=False, comment='英文名称')
        description = db.Column(db.Text, comment='分类描述')
        parent_id = db.Column(db.Integer, db.ForeignKey('equipment_categories.id'), comment='父分类ID')
        sort_order = db.Column(db.Integer, default=0, comment='排序')
        is_active = db.Column(db.Boolean, default=True, comment='是否启用')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        # 关系
        children = db.relationship('EquipmentCategory', backref=db.backref('parent', remote_side=[id]))
        equipment = db.relationship('Equipment', backref='category', lazy='dynamic')
        
        def to_dict(self):
            return {
                'id': self.id,
                'name': self.name,
                'name_en': self.name_en,
                'description': self.description,
                'parent_id': self.parent_id,
                'sort_order': self.sort_order,
                'is_active': self.is_active,
                'children': [child.to_dict() for child in self.children if child.is_active]
            }
    
    class Equipment(db.Model):
        """装备表"""
        __tablename__ = 'equipment'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(200), nullable=False, comment='装备名称')
        brand = db.Column(db.String(100), comment='品牌')
        model = db.Column(db.String(100), comment='型号')
        category_id = db.Column(db.Integer, db.ForeignKey('equipment_categories.id'), nullable=False)
        description = db.Column(db.Text, comment='装备描述')
        specifications = db.Column(db.JSON, comment='规格参数')
        images = db.Column(db.JSON, comment='装备图片')
        tags = db.Column(db.JSON, comment='标签')
        weight = db.Column(db.Float, comment='重量(克)')
        material = db.Column(db.String(200), comment='材质')
        color_options = db.Column(db.JSON, comment='颜色选项')
        size_options = db.Column(db.JSON, comment='尺寸选项')
        avg_rating = db.Column(db.Float, default=0.0, comment='平均评分')
        review_count = db.Column(db.Integer, default=0, comment='评价数量')
        is_active = db.Column(db.Boolean, default=True, comment='是否启用')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        # 关系
        prices = db.relationship('EquipmentPrice', backref='equipment', lazy='dynamic', cascade='all, delete-orphan')
        reviews = db.relationship('EquipmentReview', backref='equipment', lazy='dynamic', cascade='all, delete-orphan')
        
        # 索引
        __table_args__ = (
            Index('idx_equipment_name', 'name'),
            Index('idx_equipment_brand', 'brand'),
            Index('idx_equipment_category', 'category_id'),
            Index('idx_equipment_rating', 'avg_rating'),
        )
        
        def to_dict(self, include_prices=False, include_reviews=False):
            result = {
                'id': self.id,
                'name': self.name,
                'brand': self.brand,
                'model': self.model,
                'category_id': self.category_id,
                'category_name': self.category.name if self.category else None,
                'description': self.description,
                'specifications': self.specifications,
                'images': self.images,
                'tags': self.tags,
                'weight': self.weight,
                'material': self.material,
                'color_options': self.color_options,
                'size_options': self.size_options,
                'avg_rating': self.avg_rating,
                'review_count': self.review_count,
                'is_active': self.is_active,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None
            }
            
            if include_prices:
                latest_prices = self.prices.order_by(EquipmentPrice.created_at.desc()).limit(5).all()
                result['latest_prices'] = [price.to_dict() for price in latest_prices]
                
            if include_reviews:
                latest_reviews = self.reviews.order_by(EquipmentReview.created_at.desc()).limit(10).all()
                result['latest_reviews'] = [review.to_dict() for review in latest_reviews]
                
            return result
    
    class EquipmentPrice(db.Model):
        """装备价格表"""
        __tablename__ = 'equipment_prices'
        
        id = db.Column(db.Integer, primary_key=True)
        equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
        platform = db.Column(db.String(50), nullable=False, comment='平台名称')
        platform_url = db.Column(db.String(500), comment='商品链接')
        platform_id = db.Column(db.String(100), comment='平台商品ID')
        price = db.Column(DECIMAL(10, 2), nullable=False, comment='价格')
        original_price = db.Column(DECIMAL(10, 2), comment='原价')
        discount = db.Column(db.Float, comment='折扣')
        currency = db.Column(db.String(10), default='CNY', comment='货币')
        stock_status = db.Column(db.String(20), comment='库存状态')
        seller_name = db.Column(db.String(200), comment='卖家名称')
        seller_rating = db.Column(db.Float, comment='卖家评分')
        shipping_info = db.Column(db.JSON, comment='配送信息')
        promotion_info = db.Column(db.JSON, comment='促销信息')
        is_available = db.Column(db.Boolean, default=True, comment='是否有货')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        # 索引
        __table_args__ = (
            Index('idx_price_equipment', 'equipment_id'),
            Index('idx_price_platform', 'platform'),
            Index('idx_price_created', 'created_at'),
            Index('idx_price_equipment_platform', 'equipment_id', 'platform'),
        )
        
        def to_dict(self):
            return {
                'id': self.id,
                'equipment_id': self.equipment_id,
                'platform': self.platform,
                'platform_url': self.platform_url,
                'platform_id': self.platform_id,
                'price': float(self.price) if self.price else None,
                'original_price': float(self.original_price) if self.original_price else None,
                'discount': self.discount,
                'currency': self.currency,
                'stock_status': self.stock_status,
                'seller_name': self.seller_name,
                'seller_rating': self.seller_rating,
                'shipping_info': self.shipping_info,
                'promotion_info': self.promotion_info,
                'is_available': self.is_available,
                'created_at': self.created_at.isoformat() if self.created_at else None
            }
    
    class EquipmentReview(db.Model):
        """装备评价表"""
        __tablename__ = 'equipment_reviews'
        
        id = db.Column(db.Integer, primary_key=True)
        equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
        platform = db.Column(db.String(50), nullable=False, comment='平台名称')
        platform_review_id = db.Column(db.String(100), comment='平台评价ID')
        user_name = db.Column(db.String(100), comment='用户名')
        user_avatar = db.Column(db.String(500), comment='用户头像')
        rating = db.Column(db.Integer, nullable=False, comment='评分(1-5)')
        title = db.Column(db.String(200), comment='评价标题')
        content = db.Column(db.Text, comment='评价内容')
        images = db.Column(db.JSON, comment='评价图片')
        purchase_info = db.Column(db.JSON, comment='购买信息')
        helpful_count = db.Column(db.Integer, default=0, comment='有用数')
        reply_count = db.Column(db.Integer, default=0, comment='回复数')
        is_verified = db.Column(db.Boolean, default=False, comment='是否认证购买')
        review_date = db.Column(db.DateTime, comment='评价时间')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        # 索引
        __table_args__ = (
            Index('idx_review_equipment', 'equipment_id'),
            Index('idx_review_platform', 'platform'),
            Index('idx_review_rating', 'rating'),
            Index('idx_review_date', 'review_date'),
        )
        
        def to_dict(self):
            return {
                'id': self.id,
                'equipment_id': self.equipment_id,
                'platform': self.platform,
                'platform_review_id': self.platform_review_id,
                'user_name': self.user_name,
                'user_avatar': self.user_avatar,
                'rating': self.rating,
                'title': self.title,
                'content': self.content,
                'images': self.images,
                'purchase_info': self.purchase_info,
                'helpful_count': self.helpful_count,
                'reply_count': self.reply_count,
                'is_verified': self.is_verified,
                'review_date': self.review_date.isoformat() if self.review_date else None,
                'created_at': self.created_at.isoformat() if self.created_at else None
            }
    
    return EquipmentCategory, Equipment, EquipmentPrice, EquipmentReview

# 模块级别的变量，将在app.py中设置
EquipmentCategory = None
Equipment = None
EquipmentPrice = None
EquipmentReview = None