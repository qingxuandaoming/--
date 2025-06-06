#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试脚本
用于测试后端API接口功能
"""

import requests
import json
import time
from loguru import logger

class APITester:
    """API测试类"""
    
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def test_health_check(self):
        """测试健康检查接口"""
        logger.info("测试健康检查接口...")
        
        try:
            response = self.session.get(f'{self.base_url}/api/health')
            
            if response.status_code == 200:
                data = response.json()
                logger.success(f"健康检查通过: {data['status']}")
                return True
            else:
                logger.error(f"健康检查失败: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"健康检查异常: {str(e)}")
            return False
    
    def test_get_categories(self):
        """测试获取装备分类接口"""
        logger.info("测试获取装备分类接口...")
        
        try:
            response = self.session.get(f'{self.base_url}/api/equipment/categories')
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    categories = data['data']
                    logger.success(f"获取到 {len(categories)} 个装备分类")
                    
                    for category in categories[:3]:  # 显示前3个分类
                        logger.info(f"  - {category['name']} ({category['name_en']})")
                        if category.get('children'):
                            for child in category['children'][:2]:
                                logger.info(f"    - {child['name']}")
                    
                    return True
                else:
                    logger.error(f"获取分类失败: {data.get('message', '未知错误')}")
                    return False
            else:
                logger.error(f"获取分类失败: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"获取分类异常: {str(e)}")
            return False
    
    def test_search_equipment(self):
        """测试搜索装备接口"""
        logger.info("测试搜索装备接口...")
        
        test_cases = [
            {'keyword': '自行车', 'description': '搜索自行车'},
            {'keyword': '头盔', 'description': '搜索头盔'},
            {'category_id': 1, 'description': '按分类搜索'},
            {'min_price': 100, 'max_price': 1000, 'description': '按价格范围搜索'}
        ]
        
        for case in test_cases:
            try:
                logger.info(f"  {case['description']}...")
                
                params = {k: v for k, v in case.items() if k != 'description'}
                params.update({'page': 1, 'per_page': 5})
                
                response = self.session.get(
                    f'{self.base_url}/api/equipment/search',
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data['success']:
                        items = data['data']['items']
                        total = data['data']['total']
                        logger.success(f"    找到 {total} 个装备，显示前 {len(items)} 个")
                        
                        for item in items[:2]:
                            logger.info(f"      - {item['name']} ({item['brand']})")
                    else:
                        logger.error(f"    搜索失败: {data.get('message', '未知错误')}")
                else:
                    logger.error(f"    搜索失败: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"    搜索异常: {str(e)}")
        
        return True
    
    def test_crawl_equipment(self):
        """测试爬虫接口"""
        logger.info("测试爬虫接口...")
        
        try:
            # 启动爬虫任务
            crawl_data = {
                'platform': 'taobao',
                'category': 'helmet'
            }
            
            response = self.session.post(
                f'{self.base_url}/api/equipment/crawl',
                json=crawl_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    task_id = data['task_id']
                    logger.success(f"爬虫任务已启动，任务ID: {task_id}")
                    
                    # 检查任务状态
                    return self.test_crawl_status(task_id)
                else:
                    logger.error(f"启动爬虫失败: {data.get('message', '未知错误')}")
                    return False
            else:
                logger.error(f"启动爬虫失败: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"爬虫测试异常: {str(e)}")
            return False
    
    def test_crawl_status(self, task_id):
        """测试爬虫状态接口"""
        logger.info(f"检查爬虫任务状态: {task_id}")
        
        try:
            max_checks = 5
            for i in range(max_checks):
                response = self.session.get(
                    f'{self.base_url}/api/equipment/crawl/status/{task_id}'
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data['success']:
                        status_info = data['data']
                        status = status_info['status']
                        progress = status_info.get('progress', 0)
                        message = status_info.get('message', '')
                        
                        logger.info(f"  状态: {status}, 进度: {progress}%, 消息: {message}")
                        
                        if status in ['completed', 'failed']:
                            if status == 'completed':
                                logger.success("爬虫任务完成")
                            else:
                                logger.error("爬虫任务失败")
                            return status == 'completed'
                        
                        time.sleep(2)  # 等待2秒后再次检查
                    else:
                        logger.error(f"获取状态失败: {data.get('message', '未知错误')}")
                        return False
                else:
                    logger.error(f"获取状态失败: {response.status_code}")
                    return False
            
            logger.warning("爬虫任务仍在运行中")
            return True
            
        except Exception as e:
            logger.error(f"检查状态异常: {str(e)}")
            return False
    
    def test_equipment_prices(self, equipment_id=1):
        """测试装备价格历史接口"""
        logger.info(f"测试装备价格历史接口 (装备ID: {equipment_id})...")
        
        try:
            response = self.session.get(
                f'{self.base_url}/api/equipment/{equipment_id}/prices',
                params={'days': 30}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    price_data = data['data']
                    platform_prices = price_data['platform_prices']
                    price_trend = price_data['price_trend']
                    
                    logger.success(f"获取价格历史成功")
                    logger.info(f"  价格趋势: {price_trend['trend']}")
                    logger.info(f"  变化幅度: {price_trend['change_percent']}%")
                    
                    for platform, prices in platform_prices.items():
                        logger.info(f"  {platform}: {len(prices)} 条价格记录")
                    
                    return True
                else:
                    logger.error(f"获取价格历史失败: {data.get('message', '未知错误')}")
                    return False
            else:
                logger.error(f"获取价格历史失败: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"价格历史测试异常: {str(e)}")
            return False
    
    def test_equipment_recommendations(self, equipment_id=1):
        """测试装备推荐接口"""
        logger.info(f"测试装备推荐接口 (装备ID: {equipment_id})...")
        
        try:
            response = self.session.get(
                f'{self.base_url}/api/equipment/{equipment_id}/recommendations'
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    recommendations = data['data']
                    logger.success(f"获取到 {len(recommendations)} 个推荐装备")
                    
                    for rec in recommendations[:3]:
                        reason = rec.get('recommendation_reason', '未知')
                        logger.info(f"  - {rec['name']} (推荐理由: {reason})")
                    
                    return True
                else:
                    logger.error(f"获取推荐失败: {data.get('message', '未知错误')}")
                    return False
            else:
                logger.error(f"获取推荐失败: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"推荐测试异常: {str(e)}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        logger.info("开始API接口测试")
        logger.info("=" * 50)
        
        tests = [
            ('健康检查', self.test_health_check),
            ('获取装备分类', self.test_get_categories),
            ('搜索装备', self.test_search_equipment),
            ('装备价格历史', lambda: self.test_equipment_prices(1)),
            ('装备推荐', lambda: self.test_equipment_recommendations(1)),
            ('爬虫功能', self.test_crawl_equipment),
        ]
        
        results = []
        
        for test_name, test_func in tests:
            logger.info(f"\n{'='*20} {test_name} {'='*20}")
            
            try:
                result = test_func()
                results.append((test_name, result))
                
                if result:
                    logger.success(f"{test_name} 测试通过")
                else:
                    logger.error(f"{test_name} 测试失败")
                    
            except Exception as e:
                logger.error(f"{test_name} 测试异常: {str(e)}")
                results.append((test_name, False))
            
            time.sleep(1)  # 测试间隔
        
        # 输出测试结果汇总
        logger.info("\n" + "=" * 50)
        logger.info("测试结果汇总:")
        
        passed = 0
        total = len(results)
        
        for test_name, result in results:
            status = "✅ 通过" if result else "❌ 失败"
            logger.info(f"  {test_name}: {status}")
            if result:
                passed += 1
        
        logger.info(f"\n总计: {passed}/{total} 个测试通过")
        
        if passed == total:
            logger.success("所有测试通过！")
        else:
            logger.warning(f"有 {total - passed} 个测试失败")
        
        return passed == total

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='API接口测试工具')
    parser.add_argument('--url', default='http://localhost:5000', help='API服务地址')
    parser.add_argument('--test', choices=[
        'health', 'categories', 'search', 'prices', 'recommendations', 'crawl', 'all'
    ], default='all', help='指定测试项目')
    
    args = parser.parse_args()
    
    tester = APITester(args.url)
    
    if args.test == 'all':
        tester.run_all_tests()
    elif args.test == 'health':
        tester.test_health_check()
    elif args.test == 'categories':
        tester.test_get_categories()
    elif args.test == 'search':
        tester.test_search_equipment()
    elif args.test == 'prices':
        tester.test_equipment_prices()
    elif args.test == 'recommendations':
        tester.test_equipment_recommendations()
    elif args.test == 'crawl':
        tester.test_crawl_equipment()

if __name__ == '__main__':
    main()