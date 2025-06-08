#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试爬虫功能
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
        
        print(f"发送爬虫请求: {json.dumps(crawler_data, ensure_ascii=False)}")
        
        response = requests.post(
            f'{BASE_URL}/api/advanced-crawler/start',
            json=crawler_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"启动爬虫状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
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
        response = requests.get(f'{BASE_URL}/api/advanced-crawler/status/{task_id}', timeout=10)
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

def monitor_crawler_progress(task_id, max_wait_time=60):
    """监控爬虫进度"""
    print(f"\n=== 监控爬虫进度 (最大等待时间: {max_wait_time}秒) ===")
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time:
        status = test_crawler_status(task_id)
        if status and status.get('success'):
            task_status = status.get('data', {}).get('status', 'unknown')
            progress = status.get('data', {}).get('progress', {})
            
            print(f"\n📊 当前状态: {task_status}")
            if progress:
                print(f"进度信息: {json.dumps(progress, ensure_ascii=False)}")
            
            if task_status in ['completed', 'failed', 'stopped']:
                print(f"\n🏁 任务已结束，状态: {task_status}")
                return task_status
        
        print("⏳ 等待5秒后再次检查...")
        time.sleep(5)
    
    print(f"\n⏰ 监控超时 ({max_wait_time}秒)")
    return 'timeout'

def test_crawler_results(task_id):
    """测试爬虫结果获取"""
    print(f"\n=== 测试爬虫结果获取 (任务ID: {task_id}) ===")
    try:
        response = requests.get(f'{BASE_URL}/api/advanced-crawler/results/{task_id}', timeout=10)
        print(f"获取结果状态码: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ 爬虫结果获取成功")
            
            if results.get('success'):
                data = results.get('data', {})
                items = data.get('items', [])
                print(f"\n📊 爬取结果统计:")
                print(f"- 爬取商品数量: {len(items)}")
                print(f"- 任务状态: {data.get('status', 'unknown')}")
                
                if len(items) > 0:
                    print("\n📝 爬取的商品示例:")
                    for i, item in enumerate(items[:5]):
                        title = item.get('title', 'N/A')[:50] + '...' if len(item.get('title', '')) > 50 else item.get('title', 'N/A')
                        price = item.get('price', 'N/A')
                        platform = item.get('platform', 'N/A')
                        print(f"  {i+1}. [{platform}] {title} - ¥{price}")
                    
                    print("\n✅ 爬虫功能测试成功！数据已正确爬取和存储。")
                    return True
                else:
                    print("\n⚠️ 爬虫运行完成但未获取到数据")
                    return False
            else:
                print(f"❌ 获取结果失败: {results.get('message')}")
                return False
        else:
            print(f"❌ 获取结果失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试爬虫结果获取失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始爬虫功能测试...")
    print(f"测试时间: {datetime.now()}")
    
    # 1. 健康检查
    if not test_health_check():
        print("❌ 后端服务不可用，测试终止")
        return
    
    # 2. 启动爬虫任务
    task_id = test_start_crawler()
    if not task_id:
        print("❌ 爬虫启动失败，测试终止")
        return
    
    # 3. 监控爬虫进度
    final_status = monitor_crawler_progress(task_id, max_wait_time=120)
    
    # 4. 获取爬虫结果
    if final_status in ['completed', 'timeout']:
        success = test_crawler_results(task_id)
        if success:
            print("\n🎉 爬虫功能测试完全成功！")
        else:
            print("\n⚠️ 爬虫运行但数据获取有问题")
    else:
        print(f"\n❌ 爬虫任务未正常完成，最终状态: {final_status}")
    
    print("\n📋 测试完成！")

if __name__ == '__main__':
    main()