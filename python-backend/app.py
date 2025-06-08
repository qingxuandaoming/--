from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal
import os
from dotenv import load_dotenv
from loguru import logger

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:"
    f"{os.getenv('DB_PASSWORD', '123456')}@"
    f"{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '3306')}/"
    f"{os.getenv('DB_NAME', 'ljxz')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

db = SQLAlchemy(app)

# 使用工厂函数创建模型
from models.equipment import create_models
EquipmentCategory, Equipment, EquipmentPrice, EquipmentReview = create_models(db)

# 设置模块级别的变量
import models.equipment
models.equipment.EquipmentCategory = EquipmentCategory
models.equipment.Equipment = Equipment
models.equipment.EquipmentPrice = EquipmentPrice
models.equipment.EquipmentReview = EquipmentReview
from services.crawler_service import CrawlerService

# 初始化服务
crawler_service = CrawlerService()

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'cycling-equipment-backend'
    })

@app.route('/api/equipment/categories', methods=['GET'])
def get_categories():
    """获取装备分类"""
    try:
        from services.equipment_service import EquipmentService
        equipment_service = EquipmentService()
        categories = equipment_service.get_all_categories()
        return jsonify({
            'success': True,
            'data': categories
        })
    except Exception as e:
        logger.error(f"获取分类失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取分类失败'
        }), 500

@app.route('/api/equipment/search', methods=['GET'])
def search_equipment():
    """搜索装备"""
    try:
        from services.equipment_service import EquipmentService
        equipment_service = EquipmentService()
        
        # 获取查询参数
        keyword = request.args.get('keyword', '')
        category_id = request.args.get('category_id')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        sort_by = request.args.get('sort_by', 'rating')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        results = equipment_service.search_equipment(
            keyword=keyword,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            page=page,
            per_page=per_page
        )
        
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        logger.error(f"搜索装备失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '搜索装备失败'
        }), 500

@app.route('/api/equipment/<int:equipment_id>', methods=['GET'])
def get_equipment_detail(equipment_id):
    """获取装备详情"""
    try:
        from services.equipment_service import EquipmentService
        equipment_service = EquipmentService()
        
        equipment = equipment_service.get_equipment_detail(equipment_id)
        if not equipment:
            return jsonify({
                'success': False,
                'message': '装备不存在'
            }), 404
            
        return jsonify({
            'success': True,
            'data': equipment
        })
    except Exception as e:
        logger.error(f"获取装备详情失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取装备详情失败'
        }), 500

@app.route('/api/equipment', methods=['GET'])
def get_equipment_list():
    """获取装备列表"""
    try:
        from services.equipment_service import EquipmentService
        equipment_service = EquipmentService()
        
        # 获取查询参数
        category_id = request.args.get('category_id', type=int)
        sort_by = request.args.get('sort_by', 'rating')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        results = equipment_service.get_equipment_list(
            category_id=category_id,
            sort_by=sort_by,
            page=page,
            per_page=per_page
        )
        
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        logger.error(f"获取装备列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取装备列表失败'
        }), 500

@app.route('/api/equipment/<int:equipment_id>/prices', methods=['GET'])
def get_equipment_prices(equipment_id):
    """获取装备价格历史"""
    try:
        from services.equipment_service import EquipmentService
        equipment_service = EquipmentService()
        
        days = request.args.get('days', 30, type=int)
        prices = equipment_service.get_price_history(equipment_id, days)
        
        return jsonify({
            'success': True,
            'data': prices
        })
    except Exception as e:
        logger.error(f"获取价格历史失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取价格历史失败'
        }), 500

@app.route('/api/equipment/<int:equipment_id>/recommendations', methods=['GET'])
def get_equipment_recommendations(equipment_id):
    """获取装备推荐"""
    try:
        from services.equipment_service import EquipmentService
        equipment_service = EquipmentService()
        
        recommendations = equipment_service.get_recommendations(equipment_id)
        
        return jsonify({
            'success': True,
            'data': recommendations
        })
    except Exception as e:
        logger.error(f"获取推荐失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取推荐失败'
        }), 500

@app.route('/api/equipment/crawl', methods=['POST'])
def crawl_equipment():
    """手动触发爬虫"""
    try:
        data = request.get_json()
        platform = data.get('platform', 'all')
        category = data.get('category', 'all')
        
        # 异步执行爬虫任务
        task_id = crawler_service.start_crawl_task(platform, category)
        
        return jsonify({
            'success': True,
            'message': '爬虫任务已启动',
            'task_id': task_id
        })
    except Exception as e:
        logger.error(f"启动爬虫失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '启动爬虫失败'
        }), 500

@app.route('/api/equipment/crawl/status/<task_id>', methods=['GET'])
def get_crawl_status(task_id):
    """获取爬虫任务状态"""
    try:
        status = crawler_service.get_task_status(task_id)
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        logger.error(f"获取任务状态失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': '获取任务状态失败'
        }), 500

if __name__ == '__main__':
    with app.app_context():
        # 创建数据库表
        db.create_all()
        logger.info("数据库表创建完成")
    
    # 启动应用
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'True').lower() == 'true'
    )