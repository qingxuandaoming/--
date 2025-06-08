#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动脚本
用于启动Flask应用和调度器
"""

import os
import sys
import threading
import time
from loguru import logger
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def start_flask_app():
    """启动Flask应用"""
    try:
        from app import app
        
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('DEBUG', 'True').lower() == 'true'
        
        logger.info(f"启动Flask应用: http://{host}:{port}")
        app.run(host=host, port=port, debug=debug, use_reloader=False)
        
    except Exception as e:
        logger.error(f"启动Flask应用失败: {str(e)}")
        sys.exit(1)

def start_scheduler():
    """启动任务调度器"""
    try:
        time.sleep(5)  # 等待Flask应用启动
        
        from scheduler import TaskScheduler
        
        scheduler = TaskScheduler()
        scheduler.start()
        
        logger.info("任务调度器已启动")
        
        # 保持调度器运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("收到停止信号，正在关闭调度器...")
            scheduler.stop()
            
    except Exception as e:
        logger.error(f"启动任务调度器失败: {str(e)}")

def check_dependencies():
    """检查依赖项"""
    logger.info("检查系统依赖...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        logger.error("需要Python 3.8或更高版本")
        return False
    
    # 检查必要的包
    required_packages = {
        'flask': 'flask',
        'flask_sqlalchemy': 'flask_sqlalchemy', 
        'flask_cors': 'flask_cors',
        'pymysql': 'pymysql',
        'requests': 'requests',
        'beautifulsoup4': 'bs4',
        'selenium': 'selenium',
        'loguru': 'loguru',
        'apscheduler': 'apscheduler'
    }
    
    missing_packages = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        logger.error(f"缺少以下包: {', '.join(missing_packages)}")
        logger.error("请运行: pip install -r requirements.txt")
        return False
    
    # 检查环境变量
    required_env_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    missing_env_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_env_vars.append(var)
    
    if missing_env_vars:
        logger.warning(f"缺少环境变量: {', '.join(missing_env_vars)}")
        logger.warning("将使用默认值，请检查.env文件")
    
    logger.info("依赖检查完成")
    return True

def check_database_connection():
    """检查数据库连接"""
    try:
        import pymysql
        
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '123456'),
            database=os.getenv('DB_NAME', 'ljxz'),
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        
        connection.close()
        
        if result:
            logger.info("数据库连接正常")
            return True
        else:
            logger.error("数据库连接测试失败")
            return False
            
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        logger.error("请检查数据库配置和服务状态")
        return False

def initialize_database():
    """初始化数据库"""
    try:
        from app import app, db
        
        with app.app_context():
            # 创建所有表
            db.create_all()
            logger.info("数据库表创建/更新完成")
            
            # 检查是否需要初始化数据
            from models.equipment import EquipmentCategory
            
            category_count = EquipmentCategory.query.count()
            if category_count == 0:
                logger.info("检测到空数据库，建议运行数据初始化脚本")
                logger.info("运行命令: python init_data.py")
            else:
                logger.info(f"数据库已包含 {category_count} 个装备分类")
            
            return True
            
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        return False

def main():
    """主函数"""
    logger.info("=" * 50)
    logger.info("灵境行者 Python后端服务启动")
    logger.info("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查数据库连接
    if not check_database_connection():
        sys.exit(1)
    
    # 初始化数据库
    if not initialize_database():
        sys.exit(1)
    
    # 启动服务
    logger.info("启动服务...")
    
    # 在单独线程中启动调度器
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    
    # 启动Flask应用（主线程）
    start_flask_app()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("收到停止信号，正在关闭服务...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"启动失败: {str(e)}")
        sys.exit(1)
