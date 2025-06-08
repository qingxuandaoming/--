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
from services.advanced_crawler_service import AdvancedCrawlerService
from services.equipment_service import EquipmentService
from services.data_analysis_service import DataAnalysisService
from services.crawler_config_service import CrawlerConfigService
from services.crawler_monitor_service import CrawlerMonitorService
from services.crawler_queue_service import CrawlerQueueService, TaskStatus, TaskPriority
from services.data_validation_service import DataValidationService
# from services.recommendation_service import RecommendationService
# from services.price_alert_service import PriceAlertService

# 初始化服务
crawler_service = CrawlerService()
advanced_crawler_service = AdvancedCrawlerService()
equipment_service = EquipmentService()
data_analysis_service = DataAnalysisService()
crawler_config_service = CrawlerConfigService()
crawler_monitor_service = CrawlerMonitorService()
crawler_queue_service = CrawlerQueueService()
data_validation_service = DataValidationService()
# recommendation_service = RecommendationService()
# price_alert_service = PriceAlertService()

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
        equipment_service = EquipmentService(
            db=db,
            equipment_model=Equipment,
            category_model=EquipmentCategory,
            price_model=EquipmentPrice,
            review_model=EquipmentReview
        )
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
        equipment_service = EquipmentService(
            db=db,
            equipment_model=Equipment,
            category_model=EquipmentCategory,
            price_model=EquipmentPrice,
            review_model=EquipmentReview
        )
        
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
        equipment_service = EquipmentService(
            db=db,
            equipment_model=Equipment,
            category_model=EquipmentCategory,
            price_model=EquipmentPrice,
            review_model=EquipmentReview
        )
        
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
        equipment_service = EquipmentService(
            db=db,
            equipment_model=Equipment,
            category_model=EquipmentCategory,
            price_model=EquipmentPrice,
            review_model=EquipmentReview
        )
        
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
        equipment_service = EquipmentService(
            db=db,
            equipment_model=Equipment,
            category_model=EquipmentCategory,
            price_model=EquipmentPrice,
            review_model=EquipmentReview
        )
        
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
        equipment_service = EquipmentService(
            db=db,
            equipment_model=Equipment,
            category_model=EquipmentCategory,
            price_model=EquipmentPrice,
            review_model=EquipmentReview
        )
        
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

# 高级爬虫API
@app.route('/api/advanced-crawler/start', methods=['POST'])
def start_advanced_crawl():
    """启动高级爬虫任务"""
    try:
        data = request.get_json() or {}
        
        platforms = data.get('platforms', ['taobao', 'jd'])
        categories = data.get('categories', ['bike', 'helmet', 'clothing', 'accessories'])
        keywords = data.get('keywords')
        max_items_per_keyword = data.get('max_items_per_keyword', 50)
        
        task_id = advanced_crawler_service.start_advanced_crawl_task(
            platforms=platforms,
            categories=categories,
            keywords=keywords,
            max_items_per_keyword=max_items_per_keyword
        )
        
        return jsonify({
            'success': True,
            'message': '高级爬虫任务已启动',
            'task_id': task_id
        })
    except Exception as e:
        logger.error(f"启动高级爬虫任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'启动失败: {str(e)}'
        }), 500

@app.route('/api/advanced-crawler/status/<task_id>', methods=['GET'])
def get_advanced_crawl_status(task_id):
    """获取高级爬虫任务状态"""
    try:
        status = advanced_crawler_service.get_task_status(task_id)
        return jsonify({
            'success': True,
            'data': status
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404
    except Exception as e:
        logger.error(f"获取高级爬虫任务状态失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取状态失败: {str(e)}'
        }), 500

@app.route('/api/advanced-crawler/tasks', methods=['GET'])
def get_all_advanced_crawl_tasks():
    """获取所有高级爬虫任务"""
    try:
        tasks = advanced_crawler_service.get_all_tasks()
        return jsonify({
            'success': True,
            'data': tasks
        })
    except Exception as e:
        logger.error(f"获取高级爬虫任务列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取任务列表失败: {str(e)}'
        }), 500

# 数据分析API
@app.route('/api/analysis/trends', methods=['GET'])
def get_equipment_trends():
    """获取装备价格趋势分析"""
    try:
        days = request.args.get('days', 30, type=int)
        analysis = data_analysis_service.analyze_equipment_trends(days)
        
        return jsonify({
            'success': True,
            'data': analysis
        })
    except Exception as e:
        logger.error(f"获取装备趋势分析失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'分析失败: {str(e)}'
        }), 500

@app.route('/api/analysis/competition', methods=['GET'])
def get_market_competition():
    """获取市场竞争分析"""
    try:
        category = request.args.get('category')
        analysis = data_analysis_service.analyze_market_competition(category)
        
        return jsonify({
            'success': True,
            'data': analysis
        })
    except Exception as e:
        logger.error(f"获取市场竞争分析失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'分析失败: {str(e)}'
        }), 500

@app.route('/api/analysis/price-alerts', methods=['GET'])
def get_price_alerts():
    """获取价格预警"""
    try:
        threshold = request.args.get('threshold', 10.0, type=float)
        alerts = data_analysis_service.generate_price_alerts(threshold)
        
        return jsonify({
            'success': True,
            'data': alerts
        })
    except Exception as e:
        logger.error(f"获取价格预警失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取预警失败: {str(e)}'
        }), 500

@app.route('/api/analysis/recommendations', methods=['GET'])
def get_analysis_recommendations():
    """获取装备推荐"""
    try:
        category = request.args.get('category')
        platform = request.args.get('platform')
        min_budget = request.args.get('min_budget', type=float)
        max_budget = request.args.get('max_budget', type=float)
        limit = request.args.get('limit', 10, type=int)
        
        budget_range = None
        if min_budget is not None and max_budget is not None:
            budget_range = (min_budget, max_budget)
        
        recommendations = data_analysis_service.get_equipment_recommendations(
            category=category,
            budget_range=budget_range,
            platform=platform,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'data': recommendations
        })
    except Exception as e:
        logger.error(f"获取装备推荐失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取推荐失败: {str(e)}'
        }), 500

@app.route('/api/analysis/clear-cache', methods=['POST'])
def clear_analysis_cache():
    """清理分析缓存"""
    try:
        data_analysis_service.clear_cache()
        return jsonify({
            'success': True,
            'message': '分析缓存已清理'
        })
    except Exception as e:
        logger.error(f"清理分析缓存失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'清理缓存失败: {str(e)}'
        }), 500

# 爬虫配置管理API
@app.route('/api/config/crawler', methods=['GET'])
def get_crawler_config():
    """获取爬虫配置"""
    try:
        key_path = request.args.get('key')
        config = crawler_config_service.get_config(key_path)
        
        return jsonify({
            'success': True,
            'data': config
        })
    except Exception as e:
        logger.error(f"获取爬虫配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取配置失败: {str(e)}'
        }), 500

@app.route('/api/config/crawler', methods=['PUT'])
def update_crawler_config():
    """更新爬虫配置"""
    try:
        data = request.get_json()
        key_path = data.get('key')
        value = data.get('value')
        
        if not key_path:
            return jsonify({
                'success': False,
                'message': '缺少配置键路径'
            }), 400
        
        success = crawler_config_service.set_config(key_path, value)
        
        if success:
            return jsonify({
                'success': True,
                'message': '配置更新成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '配置更新失败'
            }), 500
    
    except Exception as e:
        logger.error(f"更新爬虫配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'更新配置失败: {str(e)}'
        }), 500

@app.route('/api/config/crawler/summary', methods=['GET'])
def get_crawler_config_summary():
    """获取爬虫配置摘要"""
    try:
        summary = crawler_config_service.get_config_summary()
        return jsonify({
            'success': True,
            'data': summary
        })
    except Exception as e:
        logger.error(f"获取爬虫配置摘要失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取配置摘要失败: {str(e)}'
        }), 500

@app.route('/api/config/crawler/platforms', methods=['GET'])
def get_enabled_platforms():
    """获取启用的平台列表"""
    try:
        platforms = crawler_config_service.get_enabled_platforms()
        return jsonify({
            'success': True,
            'data': platforms
        })
    except Exception as e:
        logger.error(f"获取启用平台列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取平台列表失败: {str(e)}'
        }), 500

@app.route('/api/config/crawler/categories', methods=['GET'])
def get_enabled_categories():
    """获取启用的分类列表"""
    try:
        categories = crawler_config_service.get_enabled_categories()
        return jsonify({
            'success': True,
            'data': categories
        })
    except Exception as e:
        logger.error(f"获取启用分类列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取分类列表失败: {str(e)}'
        }), 500

@app.route('/api/config/crawler/keywords/<category>', methods=['GET'])
def get_category_keywords(category):
    """获取分类的关键词列表"""
    try:
        keywords = crawler_config_service.get_keywords_by_category(category)
        return jsonify({
            'success': True,
            'data': keywords
        })
    except Exception as e:
        logger.error(f"获取分类关键词失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取关键词失败: {str(e)}'
        }), 500

@app.route('/api/config/crawler/keywords/<category>', methods=['POST'])
def add_category_keywords(category):
    """向分类添加关键词"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', [])
        
        if not keywords:
            return jsonify({
                'success': False,
                'message': '关键词列表不能为空'
            }), 400
        
        success = crawler_config_service.add_keywords_to_category(category, keywords)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'成功添加 {len(keywords)} 个关键词到分类 {category}'
            })
        else:
            return jsonify({
                'success': False,
                'message': '添加关键词失败'
            }), 500
    
    except Exception as e:
        logger.error(f"添加分类关键词失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'添加关键词失败: {str(e)}'
        }), 500

@app.route('/api/config/crawler/keywords/<category>', methods=['DELETE'])
def remove_category_keywords(category):
    """从分类移除关键词"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', [])
        
        if not keywords:
            return jsonify({
                'success': False,
                'message': '关键词列表不能为空'
            }), 400
        
        success = crawler_config_service.remove_keywords_from_category(category, keywords)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'成功从分类 {category} 移除 {len(keywords)} 个关键词'
            })
        else:
            return jsonify({
                'success': False,
                'message': '移除关键词失败'
            }), 500
    
    except Exception as e:
        logger.error(f"移除分类关键词失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'移除关键词失败: {str(e)}'
        }), 500

@app.route('/api/config/crawler/platform/<platform>/status', methods=['PUT'])
def update_platform_status(platform):
    """更新平台启用状态"""
    try:
        data = request.get_json()
        enabled = data.get('enabled', False)
        
        success = crawler_config_service.update_platform_status(platform, enabled)
        
        if success:
            status = '启用' if enabled else '禁用'
            return jsonify({
                'success': True,
                'message': f'平台 {platform} 已{status}'
            })
        else:
            return jsonify({
                'success': False,
                'message': '更新平台状态失败'
            }), 500
    
    except Exception as e:
        logger.error(f"更新平台状态失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'更新平台状态失败: {str(e)}'
        }), 500

@app.route('/api/config/crawler/category/<category>/status', methods=['PUT'])
def update_category_status(category):
    """更新分类启用状态"""
    try:
        data = request.get_json()
        enabled = data.get('enabled', False)
        
        success = crawler_config_service.update_category_status(category, enabled)
        
        if success:
            status = '启用' if enabled else '禁用'
            return jsonify({
                'success': True,
                'message': f'分类 {category} 已{status}'
            })
        else:
            return jsonify({
                'success': False,
                'message': '更新分类状态失败'
            }), 500
    
    except Exception as e:
        logger.error(f"更新分类状态失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'更新分类状态失败: {str(e)}'
        }), 500

@app.route('/api/config/crawler/reset', methods=['POST'])
def reset_crawler_config():
    """重置爬虫配置为默认值"""
    try:
        success = crawler_config_service.reset_to_default()
        
        if success:
            return jsonify({
                'success': True,
                'message': '爬虫配置已重置为默认值'
            })
        else:
            return jsonify({
                'success': False,
                'message': '重置配置失败'
            }), 500
    
    except Exception as e:
        logger.error(f"重置爬虫配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'重置配置失败: {str(e)}'
        }), 500

@app.route('/api/config/crawler/export', methods=['GET'])
def export_crawler_config():
    """导出爬虫配置"""
    try:
        config = crawler_config_service.get_config()
        
        return jsonify({
            'success': True,
            'data': config,
            'filename': f'crawler_config_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        })
    
    except Exception as e:
        logger.error(f"导出爬虫配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'导出配置失败: {str(e)}'
        }), 500

# 爬虫监控API
@app.route('/api/monitor/start', methods=['POST'])
def start_monitoring():
    """启动监控服务"""
    try:
        crawler_monitor_service.start_monitoring()
        return jsonify({
            'success': True,
            'message': '监控服务已启动'
        })
    except Exception as e:
        logger.error(f"启动监控服务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'启动监控失败: {str(e)}'
        }), 500

@app.route('/api/monitor/stop', methods=['POST'])
def stop_monitoring():
    """停止监控服务"""
    try:
        crawler_monitor_service.stop_monitoring()
        return jsonify({
            'success': True,
            'message': '监控服务已停止'
        })
    except Exception as e:
        logger.error(f"停止监控服务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'停止监控失败: {str(e)}'
        }), 500

@app.route('/api/monitor/stats/current', methods=['GET'])
def get_current_crawler_stats():
    """获取当前爬虫统计"""
    try:
        stats = crawler_monitor_service.get_current_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        logger.error(f"获取当前统计失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取统计失败: {str(e)}'
        }), 500

@app.route('/api/monitor/stats/history', methods=['GET'])
def get_crawler_stats_history():
    """获取爬虫统计历史"""
    try:
        limit = request.args.get('limit', 100, type=int)
        history = crawler_monitor_service.get_stats_history(limit)
        return jsonify({
            'success': True,
            'data': history
        })
    except Exception as e:
        logger.error(f"获取统计历史失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取统计历史失败: {str(e)}'
        }), 500

@app.route('/api/monitor/metrics/current', methods=['GET'])
def get_current_system_metrics():
    """获取当前系统指标"""
    try:
        metrics = crawler_monitor_service.get_system_metrics()
        return jsonify({
            'success': True,
            'data': metrics
        })
    except Exception as e:
        logger.error(f"获取系统指标失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取系统指标失败: {str(e)}'
        }), 500

@app.route('/api/monitor/metrics/history', methods=['GET'])
def get_system_metrics_history():
    """获取系统指标历史"""
    try:
        limit = request.args.get('limit', 100, type=int)
        history = crawler_monitor_service.get_metrics_history(limit)
        return jsonify({
            'success': True,
            'data': history
        })
    except Exception as e:
        logger.error(f"获取系统指标历史失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取系统指标历史失败: {str(e)}'
        }), 500

@app.route('/api/monitor/errors', methods=['GET'])
def get_error_summary():
    """获取错误摘要"""
    try:
        errors = crawler_monitor_service.get_error_summary()
        return jsonify({
            'success': True,
            'data': errors
        })
    except Exception as e:
        logger.error(f"获取错误摘要失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取错误摘要失败: {str(e)}'
        }), 500

@app.route('/api/monitor/performance', methods=['GET'])
def get_performance_summary():
    """获取性能摘要"""
    try:
        performance = crawler_monitor_service.get_performance_summary()
        return jsonify({
            'success': True,
            'data': performance
        })
    except Exception as e:
        logger.error(f"获取性能摘要失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取性能摘要失败: {str(e)}'
        }), 500

@app.route('/api/monitor/database', methods=['GET'])
def get_database_stats():
    """获取数据库统计"""
    try:
        stats = crawler_monitor_service.get_database_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        logger.error(f"获取数据库统计失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取数据库统计失败: {str(e)}'
        }), 500

@app.route('/api/monitor/report', methods=['GET'])
def get_comprehensive_report():
    """获取综合监控报告"""
    try:
        report = crawler_monitor_service.get_comprehensive_report()
        return jsonify({
            'success': True,
            'data': report
        })
    except Exception as e:
        logger.error(f"获取综合报告失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取综合报告失败: {str(e)}'
        }), 500

@app.route('/api/monitor/clear-history', methods=['POST'])
def clear_monitor_history():
    """清理监控历史数据"""
    try:
        data = request.get_json() or {}
        days = data.get('days', 30)
        
        crawler_monitor_service.clear_history(days)
        
        return jsonify({
            'success': True,
            'message': f'已清理 {days} 天前的历史数据'
        })
    except Exception as e:
        logger.error(f"清理历史数据失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'清理历史数据失败: {str(e)}'
        }), 500

# 爬虫队列管理API
@app.route('/api/queue/start', methods=['POST'])
def start_queue_service():
    """启动队列服务"""
    try:
        crawler_queue_service.start()
        return jsonify({
            'success': True,
            'message': '队列服务已启动'
        })
    except Exception as e:
        logger.error(f"启动队列服务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'启动队列服务失败: {str(e)}'
        }), 500

@app.route('/api/queue/stop', methods=['POST'])
def stop_queue_service():
    """停止队列服务"""
    try:
        crawler_queue_service.stop()
        return jsonify({
            'success': True,
            'message': '队列服务已停止'
        })
    except Exception as e:
        logger.error(f"停止队列服务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'停止队列服务失败: {str(e)}'
        }), 500

@app.route('/api/queue/tasks', methods=['POST'])
def create_crawler_task():
    """创建爬虫任务"""
    try:
        data = request.get_json()
        
        # 验证必需参数
        task_type = data.get('task_type')
        platform = data.get('platform')
        
        if not task_type or not platform:
            return jsonify({
                'success': False,
                'message': '缺少必需参数: task_type, platform'
            }), 400
        
        # 可选参数
        category = data.get('category', '')
        keywords = data.get('keywords', [])
        max_items = data.get('max_items', 100)
        priority = data.get('priority', 'NORMAL')
        max_retries = data.get('max_retries', 3)
        timeout = data.get('timeout', 3600)
        dependencies = data.get('dependencies', [])
        metadata = data.get('metadata', {})
        
        # 转换优先级
        try:
            priority_enum = TaskPriority[priority.upper()]
        except KeyError:
            return jsonify({
                'success': False,
                'message': f'无效的优先级: {priority}'
            }), 400
        
        # 创建任务
        task_id = crawler_queue_service.create_task(
            task_type=task_type,
            platform=platform,
            category=category,
            keywords=keywords,
            max_items=max_items,
            priority=priority_enum,
            max_retries=max_retries,
            timeout=timeout,
            dependencies=dependencies,
            metadata=metadata
        )
        
        return jsonify({
            'success': True,
            'data': {
                'task_id': task_id
            },
            'message': '任务创建成功'
        })
        
    except Exception as e:
        logger.error(f"创建爬虫任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'创建任务失败: {str(e)}'
        }), 500

@app.route('/api/queue/tasks', methods=['GET'])
def get_crawler_tasks():
    """获取爬虫任务列表"""
    try:
        # 查询参数
        status = request.args.get('status')
        task_type = request.args.get('task_type')
        platform = request.args.get('platform')
        limit = request.args.get('limit', 100, type=int)
        
        # 转换状态
        status_enum = None
        if status:
            try:
                status_enum = TaskStatus[status.upper()]
            except KeyError:
                return jsonify({
                    'success': False,
                    'message': f'无效的任务状态: {status}'
                }), 400
        
        # 获取任务列表
        tasks = crawler_queue_service.get_tasks(
            status=status_enum,
            task_type=task_type,
            platform=platform,
            limit=limit
        )
        
        # 转换为字典格式
        tasks_data = [task.to_dict() for task in tasks]
        
        return jsonify({
            'success': True,
            'data': tasks_data
        })
        
    except Exception as e:
        logger.error(f"获取爬虫任务列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取任务列表失败: {str(e)}'
        }), 500

@app.route('/api/queue/tasks/<task_id>', methods=['GET'])
def get_crawler_task(task_id):
    """获取单个爬虫任务"""
    try:
        task = crawler_queue_service.get_task(task_id)
        
        if not task:
            return jsonify({
                'success': False,
                'message': '任务不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'data': task.to_dict()
        })
        
    except Exception as e:
        logger.error(f"获取爬虫任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取任务失败: {str(e)}'
        }), 500

@app.route('/api/queue/tasks/<task_id>/cancel', methods=['POST'])
def cancel_crawler_task(task_id):
    """取消爬虫任务"""
    try:
        success = crawler_queue_service.cancel_task(task_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': '任务已取消'
            })
        else:
            return jsonify({
                'success': False,
                'message': '任务取消失败或任务不存在'
            }), 400
            
    except Exception as e:
        logger.error(f"取消爬虫任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'取消任务失败: {str(e)}'
        }), 500

@app.route('/api/queue/tasks/<task_id>/pause', methods=['POST'])
def pause_crawler_task(task_id):
    """暂停爬虫任务"""
    try:
        success = crawler_queue_service.pause_task(task_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': '任务已暂停'
            })
        else:
            return jsonify({
                'success': False,
                'message': '任务暂停失败或任务不存在'
            }), 400
            
    except Exception as e:
        logger.error(f"暂停爬虫任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'暂停任务失败: {str(e)}'
        }), 500

@app.route('/api/queue/tasks/<task_id>/resume', methods=['POST'])
def resume_crawler_task(task_id):
    """恢复爬虫任务"""
    try:
        success = crawler_queue_service.resume_task(task_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': '任务已恢复'
            })
        else:
            return jsonify({
                'success': False,
                'message': '任务恢复失败或任务不存在'
            }), 400
            
    except Exception as e:
        logger.error(f"恢复爬虫任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'恢复任务失败: {str(e)}'
        }), 500

@app.route('/api/queue/tasks/<task_id>/retry', methods=['POST'])
def retry_crawler_task(task_id):
    """重试爬虫任务"""
    try:
        success = crawler_queue_service.retry_task(task_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': '任务已重试'
            })
        else:
            return jsonify({
                'success': False,
                'message': '任务重试失败或任务不存在'
            }), 400
            
    except Exception as e:
        logger.error(f"重试爬虫任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'重试任务失败: {str(e)}'
        }), 500

@app.route('/api/queue/status', methods=['GET'])
def get_queue_status():
    """获取队列状态"""
    try:
        status = crawler_queue_service.get_queue_status()
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        logger.error(f"获取队列状态失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取队列状态失败: {str(e)}'
        }), 500

@app.route('/api/queue/cleanup', methods=['POST'])
def cleanup_completed_tasks():
    """清理已完成的任务"""
    try:
        data = request.get_json() or {}
        days = data.get('days', 7)
        
        cleaned_count = crawler_queue_service.clear_completed_tasks(days)
        
        return jsonify({
            'success': True,
            'data': {
                'cleaned_count': cleaned_count
            },
            'message': f'已清理 {cleaned_count} 个已完成的任务'
        })
        
    except Exception as e:
        logger.error(f"清理已完成任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'清理任务失败: {str(e)}'
        }), 500

# 数据验证API
@app.route('/api/validation/validate', methods=['POST'])
def validate_equipment_data():
    """验证装备数据"""
    try:
        data = request.get_json()
        equipment_data = data.get('equipment_data')
        
        if not equipment_data:
            return jsonify({
                'success': False,
                'message': '缺少装备数据'
            }), 400
        
        validation_result = data_validation_service.validate_equipment_data(equipment_data)
        
        return jsonify({
            'success': True,
            'data': validation_result
        })
        
    except Exception as e:
        logger.error(f"验证装备数据失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'验证失败: {str(e)}'
        }), 500

@app.route('/api/validation/batch', methods=['POST'])
def validate_batch_equipment_data():
    """批量验证装备数据"""
    try:
        data = request.get_json()
        equipment_list = data.get('equipment_list', [])
        
        if not equipment_list:
            return jsonify({
                'success': False,
                'message': '缺少装备数据列表'
            }), 400
        
        validation_results = data_validation_service.validate_batch_equipment_data(equipment_list)
        
        return jsonify({
            'success': True,
            'data': validation_results
        })
        
    except Exception as e:
        logger.error(f"批量验证装备数据失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'批量验证失败: {str(e)}'
        }), 500

@app.route('/api/validation/summary', methods=['GET'])
def get_validation_summary():
    """获取验证摘要"""
    try:
        summary = data_validation_service.get_validation_summary()
        
        return jsonify({
            'success': True,
            'data': summary
        })
        
    except Exception as e:
        logger.error(f"获取验证摘要失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取摘要失败: {str(e)}'
        }), 500

# 推荐服务API (暂时注释掉，需要安装scikit-learn)
# @app.route('/api/recommendations/equipment/<int:equipment_id>', methods=['GET'])
# def get_equipment_recommendations_by_id(equipment_id):
#     """根据装备ID获取推荐"""
#     try:
#         limit = request.args.get('limit', 10, type=int)
#         recommendations = recommendation_service.get_equipment_recommendations(equipment_id, limit)
#         
#         return jsonify({
#             'success': True,
#             'data': recommendations
#         })
#         
#     except Exception as e:
#         logger.error(f"获取装备推荐失败: {str(e)}")
#         return jsonify({
#             'success': False,
#             'message': f'获取推荐失败: {str(e)}'
#         }), 500

# @app.route('/api/recommendations/category/<category>', methods=['GET'])
# def get_category_recommendations(category):
#     """获取分类推荐"""
#     try:
#         limit = request.args.get('limit', 10, type=int)
#         recommendations = recommendation_service.get_category_recommendations(category, limit)
#         
#         return jsonify({
#             'success': True,
#             'data': recommendations
#         })
#         
#     except Exception as e:
#         logger.error(f"获取分类推荐失败: {str(e)}")
#         return jsonify({
#             'success': False,
#             'message': f'获取分类推荐失败: {str(e)}'
#         }), 500

@app.route('/api/recommendations/price-range', methods=['GET'])
def get_price_range_recommendations():
    """获取价格区间推荐"""
    try:
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        category = request.args.get('category')
        limit = request.args.get('limit', 10, type=int)
        
        if min_price is None or max_price is None:
            return jsonify({
                'success': False,
                'message': '缺少价格区间参数'
            }), 400
        
        recommendations = recommendation_service.get_price_range_recommendations(
            min_price, max_price, category, limit
        )
        
        return jsonify({
            'success': True,
            'data': recommendations
        })
        
    except Exception as e:
        logger.error(f"获取价格区间推荐失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取价格区间推荐失败: {str(e)}'
        }), 500

@app.route('/api/recommendations/trending', methods=['GET'])
def get_trending_recommendations():
    """获取热门推荐"""
    try:
        days = request.args.get('days', 7, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        recommendations = recommendation_service.get_trending_recommendations(days, limit)
        
        return jsonify({
            'success': True,
            'data': recommendations
        })
        
    except Exception as e:
        logger.error(f"获取热门推荐失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取热门推荐失败: {str(e)}'
        }), 500

@app.route('/api/recommendations/stats', methods=['GET'])
def get_recommendation_stats():
    """获取推荐统计"""
    try:
        stats = recommendation_service.get_recommendation_stats()
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        logger.error(f"获取推荐统计失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取推荐统计失败: {str(e)}'
        }), 500

# 价格预警API
@app.route('/api/alerts', methods=['POST'])
def create_price_alert():
    """创建价格预警"""
    try:
        data = request.get_json()
        
        required_fields = ['equipment_id', 'alert_type', 'threshold_value']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'缺少必需字段: {field}'
                }), 400
        
        alert_id = price_alert_service.create_alert(
            equipment_id=data['equipment_id'],
            alert_type=data['alert_type'],
            threshold_value=data['threshold_value'],
            user_id=data.get('user_id'),
            email=data.get('email'),
            webhook_url=data.get('webhook_url')
        )
        
        return jsonify({
            'success': True,
            'data': {'alert_id': alert_id},
            'message': '价格预警创建成功'
        })
        
    except Exception as e:
        logger.error(f"创建价格预警失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'创建预警失败: {str(e)}'
        }), 500

@app.route('/api/alerts/<int:alert_id>', methods=['GET'])
def get_price_alert(alert_id):
    """获取价格预警详情"""
    try:
        alert = price_alert_service.get_alert(alert_id)
        
        if not alert:
            return jsonify({
                'success': False,
                'message': '预警不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'data': alert
        })
        
    except Exception as e:
        logger.error(f"获取价格预警失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取预警失败: {str(e)}'
        }), 500

@app.route('/api/alerts/<int:alert_id>', methods=['PUT'])
def update_price_alert(alert_id):
    """更新价格预警"""
    try:
        data = request.get_json()
        
        success = price_alert_service.update_alert(alert_id, **data)
        
        if not success:
            return jsonify({
                'success': False,
                'message': '预警不存在或更新失败'
            }), 404
        
        return jsonify({
            'success': True,
            'message': '价格预警更新成功'
        })
        
    except Exception as e:
        logger.error(f"更新价格预警失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'更新预警失败: {str(e)}'
        }), 500

@app.route('/api/alerts/<int:alert_id>', methods=['DELETE'])
def delete_price_alert(alert_id):
    """删除价格预警"""
    try:
        success = price_alert_service.delete_alert(alert_id)
        
        if not success:
            return jsonify({
                'success': False,
                'message': '预警不存在或删除失败'
            }), 404
        
        return jsonify({
            'success': True,
            'message': '价格预警删除成功'
        })
        
    except Exception as e:
        logger.error(f"删除价格预警失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'删除预警失败: {str(e)}'
        }), 500

@app.route('/api/alerts/user/<user_id>', methods=['GET'])
def get_user_alerts(user_id):
    """获取用户的价格预警"""
    try:
        alerts = price_alert_service.get_user_alerts(user_id)
        
        return jsonify({
            'success': True,
            'data': alerts
        })
        
    except Exception as e:
        logger.error(f"获取用户价格预警失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取用户预警失败: {str(e)}'
        }), 500

@app.route('/api/alerts/history', methods=['GET'])
def get_alert_history():
    """获取预警历史"""
    try:
        alert_id = request.args.get('alert_id', type=int)
        user_id = request.args.get('user_id')
        days = request.args.get('days', 30, type=int)
        
        history = price_alert_service.get_alert_history(
            alert_id=alert_id,
            user_id=user_id,
            days=days
        )
        
        return jsonify({
            'success': True,
            'data': history
        })
        
    except Exception as e:
        logger.error(f"获取预警历史失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取预警历史失败: {str(e)}'
        }), 500

@app.route('/api/alerts/stats', methods=['GET'])
def get_alert_stats():
    """获取预警统计"""
    try:
        stats = price_alert_service.get_alert_stats()
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        logger.error(f"获取预警统计失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取预警统计失败: {str(e)}'
        }), 500

@app.route('/api/alerts/start-monitoring', methods=['POST'])
def start_alert_monitoring():
    """启动价格监控"""
    try:
        price_alert_service.start_monitoring()
        
        return jsonify({
            'success': True,
            'message': '价格监控已启动'
        })
        
    except Exception as e:
        logger.error(f"启动价格监控失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'启动监控失败: {str(e)}'
        }), 500

@app.route('/api/alerts/stop-monitoring', methods=['POST'])
def stop_alert_monitoring():
    """停止价格监控"""
    try:
        price_alert_service.stop_monitoring()
        
        return jsonify({
            'success': True,
            'message': '价格监控已停止'
        })
        
    except Exception as e:
        logger.error(f"停止价格监控失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'停止监控失败: {str(e)}'
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