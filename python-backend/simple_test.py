#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的API测试脚本
"""

import requests
import json
from datetime import datetime

# 后端API基础URL
BASE_URL = 'http://localhost:5000'

def test_api_endpoint(endpoint, method='GET', data=None):
    """通用API测试函数"""
    try:
        if method == 'GET':
            response = requests.get(f'{BASE_URL}{endpoint}')
        elif method == 'POST':
            response = requests.post(f'{BASE_URL}{endpoint}', json=data)
        
        print(f"\n{method} {endpoint}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}...")
                return True
            except:
                print(f"响应: {response.text[:200]}...")
                return True
        else:
            print(f"错误: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试API端点...")
    print(f"测试时间: {datetime.now()}")
    
    # 测试的API端点列表
    test_endpoints = [
        # 基础功能
        ('/api/health', 'GET'),
        
        # 装备相关
        ('/api/equipment/categories', 'GET'),
        ('/api/equipment/search?keyword=自行车&limit=5', 'GET'),
        ('/api/equipment', 'GET'),
        
        # 爬虫配置
        ('/api/config/crawler', 'GET'),
        ('/api/config/crawler/summary', 'GET'),
        ('/api/config/crawler/platforms', 'GET'),
        ('/api/config/crawler/categories', 'GET'),
        
        # 高级爬虫
        ('/api/advanced-crawler/tasks', 'GET'),
        
        # 监控
        ('/api/monitor/stats/current', 'GET'),
        ('/api/monitor/database', 'GET'),
        
        # 队列
        ('/api/queue/status', 'GET'),
        ('/api/queue/tasks', 'GET'),
        
        # 推荐
        ('/api/recommendations/trending', 'GET'),
        ('/api/recommendations/stats', 'GET'),
    ]
    
    success_count = 0
    total_count = len(test_endpoints)
    
    for endpoint, method in test_endpoints:
        if test_api_endpoint(endpoint, method):
            success_count += 1
    
    print(f"\n=== 测试结果总结 ===")
    print(f"总测试数: {total_count}")
    print(f"成功数: {success_count}")
    print(f"失败数: {total_count - success_count}")
    print(f"成功率: {success_count/total_count*100:.1f}%")
    
    if success_count > total_count * 0.8:
        print("✅ 大部分API端点工作正常")
    elif success_count > total_count * 0.5:
        print("⚠️ 部分API端点存在问题")
    else:
        print("❌ 多数API端点存在问题")
    
    # 测试启动爬虫
    print("\n=== 测试启动高级爬虫 ===")
    crawler_data = {
        'platforms': ['taobao'],
        'categories': ['bike'],
        'keywords': ['山地车'],
        'max_items_per_keyword': 3
    }
    
    if test_api_endpoint('/api/advanced-crawler/start', 'POST', crawler_data):
        print("✅ 爬虫启动接口正常")
    else:
        print("❌ 爬虫启动接口异常")
    
    print("\n测试完成！")

if __name__ == '__main__':
    main()