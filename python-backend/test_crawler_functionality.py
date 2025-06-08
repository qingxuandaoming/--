#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
爬虫功能测试脚本
测试爬虫服务的各项功能，包括数据爬取和存储
"""

import requests
import json
import time
from datetime import datetime
from loguru import logger

# 配置日志
logger.add("crawler_test.log", rotation="1 MB")

class CrawlerTester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_health_check(self):
        """测试健康检查接口"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                logger.info(f"健康检查成功: {data}")
                return True
            else:
                logger.error(f"健康检查失败: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"健康检查异常: {str(e)}")
            return False
    
    def test_crawler_config(self):
        """测试爬虫配置接口"""
        try:
            # 获取爬虫配置
            response = self.session.get(f"{self.base_url}/api/config/crawler")
            if response.status_code == 200:
                config = response.json()
                logger.info(f"获取爬虫配置成功: {config.get('success', False)}")
                return True
            else:
                logger.error(f"获取爬虫配置失败: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"测试爬虫配置异常: {str(e)}")
            return False
    
    def test_crawler_start(self):
        """测试启动爬虫"""
        try:
            # 启动基础爬虫任务
            data = {
                "platform": "jd",
                "category": "bike"
            }
            response = self.session.post(
                f"{self.base_url}/api/crawler/start",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"启动爬虫成功: {result}")
                return result.get('task_id')
            else:
                logger.error(f"启动爬虫失败: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"测试启动爬虫异常: {str(e)}")
            return None
    
    def test_advanced_crawler_start(self):
        """测试启动高级爬虫"""
        try:
            # 启动高级爬虫任务
            data = {
                "platforms": ["jd"],
                "categories": ["bike"],
                "keywords": ["自行车"],
                "max_items_per_keyword": 5
            }
            response = self.session.post(
                f"{self.base_url}/api/advanced-crawler/start",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"启动高级爬虫成功: {result}")
                return result.get('task_id')
            else:
                logger.error(f"启动高级爬虫失败: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"测试启动高级爬虫异常: {str(e)}")
            return None
    
    def test_crawler_status(self, task_id):
        """测试爬虫状态查询"""
        try:
            response = self.session.get(f"{self.base_url}/api/crawler/status/{task_id}")
            if response.status_code == 200:
                status = response.json()
                logger.info(f"爬虫状态: {status}")
                return status
            else:
                logger.error(f"获取爬虫状态失败: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"测试爬虫状态异常: {str(e)}")
            return None
    
    def test_equipment_data(self):
        """测试装备数据查询"""
        try:
            # 测试获取分类
            response = self.session.get(f"{self.base_url}/api/equipment/categories")
            if response.status_code == 200:
                categories = response.json()
                logger.info(f"获取装备分类成功: {len(categories.get('data', []))} 个分类")
            
            # 测试搜索装备
            response = self.session.get(f"{self.base_url}/api/equipment/search?keyword=自行车&limit=5")
            if response.status_code == 200:
                equipment = response.json()
                logger.info(f"搜索装备成功: {len(equipment.get('data', []))} 个结果")
                return True
            else:
                logger.error(f"搜索装备失败: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"测试装备数据异常: {str(e)}")
            return False
    
    def run_full_test(self):
        """运行完整测试"""
        logger.info("开始爬虫功能测试...")
        
        # 1. 健康检查
        logger.info("1. 测试健康检查...")
        if not self.test_health_check():
            logger.error("健康检查失败，停止测试")
            return False
        
        # 2. 测试配置
        logger.info("2. 测试爬虫配置...")
        if not self.test_crawler_config():
            logger.error("爬虫配置测试失败")
        
        # 3. 测试装备数据
        logger.info("3. 测试装备数据查询...")
        if not self.test_equipment_data():
            logger.error("装备数据测试失败")
        
        # 4. 测试基础爬虫启动
        logger.info("4. 测试基础爬虫启动...")
        task_id = self.test_crawler_start()
        if task_id:
            logger.info(f"基础爬虫任务启动成功，任务ID: {task_id}")
            
            # 等待一段时间后检查状态
            time.sleep(3)
            
            # 5. 测试状态查询
            logger.info("5. 测试基础爬虫状态查询...")
            status = self.test_crawler_status(task_id)
            if status:
                logger.info(f"基础爬虫状态查询成功: {status.get('data', {})}")
        
        # 6. 测试高级爬虫启动
        logger.info("6. 测试高级爬虫启动...")
        advanced_task_id = self.test_advanced_crawler_start()
        if advanced_task_id:
            logger.info(f"高级爬虫任务启动成功，任务ID: {advanced_task_id}")
            
            # 等待一段时间后检查状态
            time.sleep(3)
            
            # 7. 测试高级爬虫状态查询
            logger.info("7. 测试高级爬虫状态查询...")
            response = self.session.get(f"{self.base_url}/api/advanced-crawler/status/{advanced_task_id}")
            if response.status_code == 200:
                status = response.json()
                logger.info(f"高级爬虫状态查询成功: {status.get('data', {})}")
            
            # 等待爬虫完成（缩短等待时间）
            logger.info("等待爬虫任务完成...")
            for i in range(10):  # 最多等待10次，每次3秒
                time.sleep(3)
                status = self.test_crawler_status(task_id) if task_id else None
                if status and status.get('data', {}).get('status') in ['completed', 'failed']:
                    logger.info(f"基础爬虫任务完成，最终状态: {status.get('data', {})}")
                    break
                logger.info(f"等待中... ({i+1}/10)")
        
        logger.info("爬虫功能测试完成")
        return True

def main():
    """主函数"""
    print("=" * 50)
    print("爬虫功能测试开始")
    print(f"测试时间: {datetime.now()}")
    print("=" * 50)
    
    tester = CrawlerTester()
    success = tester.run_full_test()
    
    print("=" * 50)
    print(f"测试结果: {'成功' if success else '失败'}")
    print("=" * 50)
    
    return success

if __name__ == "__main__":
    main()