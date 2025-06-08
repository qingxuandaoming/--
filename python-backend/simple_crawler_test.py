#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的爬虫功能测试脚本
"""

import requests
import json
import time
from datetime import datetime

# 后端API基础URL
BASE_URL = 'http://localhost:5000'

def test_health_check():
    """测试健康检查接口"""
    print("\n=== 测试健康检查接口 ===")
    try:
        response = requests.get(f'{BASE_URL}/api/health')
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"响应: {response.json()}")
            print("✅ 后端服务正常")
            return True
        else:
            print(f"❌ 健康检查失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_crawler_config():
    """测试爬虫配置接口"""
    print("\n=== 测试爬虫配置接口 ===")
    try:
        # 获取爬虫配置
        response = requests.get(f'{BASE_URL}/api/config/crawler')
        print(f"获取配置状态码: {response.status_code}")
        if response.status_code == 200:
            config = response.json()
            print(f"✅ 配置获取成功")
            print(f"配置数据: {json.dumps(config, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"❌ 获取配置失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 测试爬虫配置失败: {e}")
        return False

def test_start_crawler():
    """测试启动爬虫"""
    print("\n=== 测试启动爬虫 ===")
    try:
        # 启动高级爬虫任务
        crawler_data = {
            'platforms': ['taobao'],  # 只测试淘宝平台
            'categories': ['bike'],   # 只测试自行车分类
            'keywords': ['山地车'],  # 测试关键词
            'max_items_per_keyword': 3  # 限制数量避免过度爬取
        }
        
        response = requests.post(
            f'{BASE_URL}/api/advanced-crawler/start',
            json=crawler_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"启动爬虫状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                task_id = result.get('task_id')
                print(f"✅ 爬虫任务已启动，任务ID: {task_id}")
                return task_id
            else:
                print(f"❌ 启动失败: {result.get('message')}")
                return None
        else:
            print(f"❌ 启动爬虫失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 测试启动爬虫失败: {e}")
        return None

def test_crawler_status(task_id):
    """测试爬虫状态查询"""
    print(f"\n=== 测试爬虫状态查询 (任务ID: {task_id}) ===")
    try:
        response = requests.get(f'{BASE_URL}/api/advanced-crawler/status/{task_id}')
        print(f"查询状态码: {response.status_code}")
        
        if response.status_code == 200:
            status = response.json()
            print(f"✅ 任务状态查询成功")
            print(f"状态信息: {json.dumps(status, indent=2, ensure_ascii=False)}")
            return status
        else:
            print(f"❌ 查询状态失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 测试爬虫状态查询失败: {e}")
        return None

def test_crawler_results(task_id):
    """测试爬虫结果获取"""
    print(f"\n=== 测试爬虫结果获取 (任务ID: {task_id}) ===")
    try:
        response = requests.get(f'{BASE_URL}/api/advanced-crawler/results/{task_id}')
        print(f"获取结果状态码: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ 爬虫结果获取成功")
            print(f"结果数据: {json.dumps(results, indent=2, ensure_ascii=False)}")
            return results
        else:
            print(f"❌ 获取结果失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 测试爬虫结果获取失败: {e}")
        return None

def main():
    """主测试函数"""
    print("开始爬虫功能测试...")
    print(f"测试时间: {datetime.now()}")
    
    # 1. 健康检查
    if not test_health_check():
        print("❌ 后端服务不可用，测试终止")
        return
    
    # 2. 测试爬虫配置
    if not test_crawler_config():
        print("❌ 爬虫配置测试失败")
        return
    
    # 3. 启动爬虫任务
    task_id = test_start_crawler()
    if not task_id:
        print("❌ 爬虫启动失败，测试终止")
        return
    
    # 4. 等待一段时间让爬虫运行
    print("\n⏳ 等待爬虫运行...")
    time.sleep(10)
    
    # 5. 查询爬虫状态
    status = test_crawler_status(task_id)
    if status:
        print(f"当前状态: {status.get('data', {}).get('status', 'unknown')}")
    
    # 6. 获取爬虫结果
    results = test_crawler_results(task_id)
    if results:
        data = results.get('data', {})
        items_count = len(data.get('items', []))
        print(f"\n📊 爬取结果统计:")
        print(f"- 爬取商品数量: {items_count}")
        print(f"- 任务状态: {data.get('status', 'unknown')}")
        
        if items_count > 0:
            print("\n✅ 爬虫功能测试成功！")
            print("\n📝 爬取的商品示例:")
            for i, item in enumerate(data.get('items', [])[:3]):
                print(f"  {i+1}. {item.get('title', 'N/A')} - ¥{item.get('price', 'N/A')}")
        else:
            print("\n⚠️ 爬虫运行完成但未获取到数据")
    else:
        print("\n❌ 无法获取爬虫结果")
    
    print("\n测试完成！")

if __name__ == '__main__':
    main()