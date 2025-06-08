#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强爬虫系统部署脚本
自动设置和初始化新增的爬虫功能
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("检查Python版本...")
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    print(f"✅ Python版本: {sys.version}")
    return True

def install_dependencies():
    """安装依赖包"""
    print("\n安装依赖包...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def check_env_file():
    """检查环境配置文件"""
    print("\n检查环境配置...")
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists():
        if env_example.exists():
            print("复制.env.example到.env...")
            with open(env_example, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ 已创建.env文件")
        else:
            print("创建默认.env文件...")
            default_env = """
# 数据库配置
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/crawler_db

# Flask配置
FLASK_ENV=development
DEBUG=True
HOST=0.0.0.0
PORT=5000

# 爬虫配置
CRAWLER_DELAY=1
CRAWLER_TIMEOUT=30
CRAWLER_RETRIES=3

# Redis配置（可选）
REDIS_URL=redis://localhost:6379/0

# 邮件配置（用于价格预警）
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/crawler.log
"""
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(default_env)
            print("✅ 已创建默认.env文件")
    else:
        print("✅ .env文件已存在")
    
    return True

def create_directories():
    """创建必要的目录"""
    print("\n创建必要目录...")
    directories = [
        'logs',
        'data',
        'cache',
        'exports'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ 创建目录: {directory}")
    
    return True

def init_database():
    """初始化数据库"""
    print("\n初始化数据库...")
    try:
        # 运行数据库初始化脚本
        if Path('init_data.py').exists():
            subprocess.run([sys.executable, 'init_data.py'], check=True)
            print("✅ 数据库初始化完成")
        else:
            print("⚠️ 未找到init_data.py，请手动初始化数据库")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False

def test_services():
    """测试服务功能"""
    print("\n测试服务功能...")
    try:
        # 导入并测试服务
        sys.path.append(os.getcwd())
        
        # 测试数据验证服务
        from services.data_validation_service import DataValidationService
        validation_service = DataValidationService()
        print("✅ 数据验证服务初始化成功")
        
        # 测试推荐服务
        from services.recommendation_service import RecommendationService
        recommendation_service = RecommendationService()
        print("✅ 推荐服务初始化成功")
        
        # 测试价格预警服务
        from services.price_alert_service import PriceAlertService
        alert_service = PriceAlertService()
        print("✅ 价格预警服务初始化成功")
        
        return True
    except ImportError as e:
        print(f"❌ 服务导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 服务测试失败: {e}")
        return False

def start_application():
    """启动应用"""
    print("\n启动Flask应用...")
    print("应用将在 http://localhost:5000 启动")
    print("按 Ctrl+C 停止应用")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n应用已停止")
    except Exception as e:
        print(f"❌ 应用启动失败: {e}")

def show_api_endpoints():
    """显示API端点信息"""
    print("\n📋 新增API端点列表:")
    print("-" * 50)
    
    endpoints = [
        ("数据验证API", [
            "POST /api/validation/validate - 验证单个装备数据",
            "POST /api/validation/batch - 批量验证装备数据",
            "GET /api/validation/summary - 获取验证摘要"
        ]),
        ("推荐服务API", [
            "GET /api/recommendations/equipment/<id> - 根据装备ID获取推荐",
            "GET /api/recommendations/category/<category> - 获取分类推荐",
            "GET /api/recommendations/price-range - 获取价格区间推荐",
            "GET /api/recommendations/trending - 获取热门推荐",
            "GET /api/recommendations/stats - 获取推荐统计"
        ]),
        ("价格预警API", [
            "POST /api/alerts - 创建价格预警",
            "GET /api/alerts/<id> - 获取价格预警详情",
            "PUT /api/alerts/<id> - 更新价格预警",
            "DELETE /api/alerts/<id> - 删除价格预警",
            "GET /api/alerts/user/<user_id> - 获取用户预警",
            "GET /api/alerts/history - 获取预警历史",
            "GET /api/alerts/stats - 获取预警统计",
            "POST /api/alerts/start-monitoring - 启动价格监控",
            "POST /api/alerts/stop-monitoring - 停止价格监控"
        ])
    ]
    
    for category, apis in endpoints:
        print(f"\n{category}:")
        for api in apis:
            print(f"  • {api}")
    
    print("\n💡 使用 test_new_apis.py 脚本测试这些API")

def main():
    """主函数"""
    print("🚀 增强爬虫系统部署脚本")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 安装依赖
    if not install_dependencies():
        print("\n请手动安装依赖: pip install -r requirements.txt")
        return
    
    # 检查环境配置
    if not check_env_file():
        return
    
    # 创建目录
    if not create_directories():
        return
    
    # 初始化数据库
    init_database()
    
    # 测试服务
    if not test_services():
        print("\n⚠️ 服务测试失败，但可以继续启动应用")
    
    # 显示API端点
    show_api_endpoints()
    
    print("\n🎉 部署完成！")
    print("\n选择操作:")
    print("1. 启动Flask应用")
    print("2. 运行API测试")
    print("3. 退出")
    
    while True:
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == '1':
            start_application()
            break
        elif choice == '2':
            print("\n运行API测试...")
            try:
                subprocess.run([sys.executable, 'test_new_apis.py'])
            except Exception as e:
                print(f"❌ 测试运行失败: {e}")
            break
        elif choice == '3':
            print("\n👋 再见！")
            break
        else:
            print("❌ 无效选择，请输入1-3")

if __name__ == '__main__':
    main()