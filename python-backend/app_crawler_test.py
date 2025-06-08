#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

# 导入爬虫相关服务
from services.crawler_service import CrawlerService
from services.advanced_crawler_service import AdvancedCrawlerService
from services.equipment_service import EquipmentService
from services.data_analysis_service import DataAnalysisService
from services.crawler_config_service import CrawlerConfigService
from services.crawler_monitor_service import CrawlerMonitorService
from services.crawler_queue_service import CrawlerQueueService, TaskStatus, TaskPriority
from services.data_validation_service import DataValidationService

# 初始化服务
crawler_service = CrawlerService()
advanced_crawler_service = AdvancedCrawlerService()
equipment_service = EquipmentService()
data_analysis_service = DataAnalysisService()
crawler_config_service = CrawlerConfigService()
crawler_monitor_service = CrawlerMonitorService()
crawler_queue_service = CrawlerQueueService()
data_validation_service = DataValidationService()

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'cycling-equipment-backend'
    })

# 爬虫配置API
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

# API配置管理
@app.route('/api/crawler/api-config', methods=['GET'])
def get_api_config():
    """获取API配置状态"""
    try:
        status = crawler_service.get_api_status()
        return jsonify({
            'success': True,
            'data': status
        })
    except Exception as e:
        logger.error(f"获取API配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取API配置失败: {str(e)}'
        }), 500

@app.route('/api/crawler/api-config', methods=['POST'])
def configure_api():
    """配置第三方API"""
    try:
        data = request.get_json()
        provider = data.get('provider')
        app_key = data.get('app_key')
        app_secret = data.get('app_secret')
        
        if not provider or not app_key:
            return jsonify({
                'success': False,
                'message': '缺少必需参数: provider 和 app_key'
            }), 400
        
        success = crawler_service.configure_api(provider, app_key, app_secret)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'{provider} API配置成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '不支持的API提供商'
            }), 400
            
    except Exception as e:
        logger.error(f"配置API失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'配置API失败: {str(e)}'
        }), 500

@app.route('/api/crawler/crawl-method', methods=['GET'])
def get_crawl_methods():
    """获取爬取方式配置"""
    try:
        methods = crawler_service.crawl_methods
        return jsonify({
            'success': True,
            'data': methods
        })
    except Exception as e:
        logger.error(f"获取爬取方式配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取爬取方式配置失败: {str(e)}'
        }), 500

@app.route('/api/crawler/crawl-method', methods=['PUT'])
def set_crawl_method():
    """设置爬取方式"""
    try:
        data = request.get_json()
        method = data.get('method')
        enabled = data.get('enabled')
        
        if method is None or enabled is None:
            return jsonify({
                'success': False,
                'message': '缺少必需参数: method 和 enabled'
            }), 400
        
        success = crawler_service.set_crawl_method(method, enabled)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'爬取方式设置成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': '不支持的爬取方式'
            }), 400
            
    except Exception as e:
        logger.error(f"设置爬取方式失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'设置爬取方式失败: {str(e)}'
        }), 500

# 基础爬虫API
@app.route('/api/crawler/start', methods=['POST'])
def start_crawler():
    """启动基础爬虫任务"""
    try:
        data = request.get_json() or {}
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

@app.route('/api/crawler/status/<task_id>', methods=['GET'])
def get_crawler_status(task_id):
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
def start_advanced_crawler():
    """启动高级爬虫任务"""
    try:
        data = request.get_json()
        
        # 验证必需参数
        required_fields = ['platforms', 'categories', 'keywords']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'缺少必需字段: {field}'
                }), 400
        
        # 启动爬虫任务
        task_id = advanced_crawler_service.start_crawling_task(
            platforms=data['platforms'],
            categories=data['categories'],
            keywords=data['keywords'],
            max_items_per_keyword=data.get('max_items_per_keyword', 50),
            enable_price_tracking=data.get('enable_price_tracking', True),
            enable_review_crawling=data.get('enable_review_crawling', False)
        )
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': '爬虫任务已启动'
        })
        
    except Exception as e:
        logger.error(f"启动高级爬虫失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'启动爬虫失败: {str(e)}'
        }), 500

@app.route('/api/advanced-crawler/status/<task_id>', methods=['GET'])
def get_advanced_crawler_status(task_id):
    """获取高级爬虫任务状态"""
    try:
        status = advanced_crawler_service.get_task_status(task_id)
        
        if status:
            return jsonify({
                'success': True,
                'data': status
            })
        else:
            return jsonify({
                'success': False,
                'message': '任务不存在'
            }), 404
            
    except Exception as e:
        logger.error(f"获取爬虫状态失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取状态失败: {str(e)}'
        }), 500

@app.route('/api/advanced-crawler/stop/<task_id>', methods=['POST'])
def stop_advanced_crawler(task_id):
    """停止高级爬虫任务"""
    try:
        success = advanced_crawler_service.stop_task(task_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': '任务已停止'
            })
        else:
            return jsonify({
                'success': False,
                'message': '停止任务失败'
            }), 500
            
    except Exception as e:
        logger.error(f"停止爬虫任务失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'停止任务失败: {str(e)}'
        }), 500

@app.route('/api/advanced-crawler/results/<task_id>', methods=['GET'])
def get_advanced_crawler_results(task_id):
    """获取高级爬虫任务结果"""
    try:
        results = advanced_crawler_service.get_task_results(task_id)
        
        if results:
            return jsonify({
                'success': True,
                'data': results
            })
        else:
            return jsonify({
                'success': False,
                'message': '任务结果不存在'
            }), 404
            
    except Exception as e:
        logger.error(f"获取爬虫结果失败: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'获取结果失败: {str(e)}'
        }), 500

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            logger.info("数据库表创建成功")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)