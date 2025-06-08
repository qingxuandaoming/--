#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬虫功能测试脚本
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
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"健康检查失败: {e}")
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
            print(f"当前配置: {json.dumps(config, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"获取配置失败: {response.text}")
            return False
    except Exception as e:
        print(f"测试爬虫配置失败: {e}")
        return False

def test_start_crawler():
    """测试启动爬虫"""
    print("\n=== 测试启动爬虫 ===")
    try:
        # 启动高级爬虫任务
        crawler_data = {
            'platforms': ['taobao'],  # 只测试淘宝平台
            'categories': ['bike'],   # 只测试自行车分类
            'keywords': ['山地车', '自行车'],  # 测试关键词
            'max_items_per_keyword': 5  # 限制数量避免过度爬取
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
                print(f"爬虫任务已启动，任务ID: {task_id}")
                return task_id
            else:
                print(f"启动失败: {result.get('message')}")
                return None
        else:
            print(f"启动爬虫失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"测试启动爬虫失败: {e}")
        return None

def test_crawler_status(task_id):
    """测试爬虫状态查询"""
    print(f"\n=== 测试爬虫状态查询 (任务ID: {task_id}) ===")
    try:
        response = requests.get(f'{BASE_URL}/api/advanced-crawler/status/{task_id}')
        print(f"查询状态码: {response.status_code}")
        
        if response.status_code == 200:
            status = response.json()
            print(f"任务状态: {json.dumps(status, indent=2, ensure_ascii=False)}")
            return status
        else:
            print(f"查询状态失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"测试爬虫状态查询失败: {e}")
        return None

def test_get_all_tasks():
    """测试获取所有爬虫任务"""
    print("\n=== 测试获取所有爬虫任务 ===")
    try:
        response = requests.get(f'{BASE_URL}/api/advanced-crawler/tasks')
        print(f"获取任务列表状态码: {response.status_code}")
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"任务列表: {json.dumps(tasks, indent=2, ensure_ascii=False)}")
            return tasks
        else:
            print(f"获取任务列表失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"测试获取任务列表失败: {e}")
        return None

def test_equipment_search():
    """测试装备搜索功能"""
    print("\n=== 测试装备搜索功能 ===")
    try:
        # 搜索装备
        params = {
            'keyword': '自行车',
            'limit': 5
        }
        
        response = requests.get(f'{BASE_URL}/api/equipment/search', params=params)
        print(f"搜索状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"搜索结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return result
        else:
            print(f"搜索失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"测试装备搜索失败: {e}")
        return None

def monitor_crawler_progress(task_id, max_wait_time=60):
    """监控爬虫进度"""
    print(f"\n=== 监控爬虫进度 (最大等待时间: {max_wait_time}秒) ===")
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time:
        status = test_crawler_status(task_id)
        if status and status.get('success'):
            task_status = status.get('data', {}).get('status')
            progress = status.get('data', {}).get('progress', 0)
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 状态: {task_status}, 进度: {progress}%")
            
            if task_status in ['completed', 'failed']:
                print(f"任务已结束，最终状态: {task_status}")
                return status
                
        time.sleep(5)  # 每5秒检查一次
    
    print("监控超时")
    return None

def main():
    """主测试函数"""
    print("开始测试爬虫功能...")
    print(f"测试时间: {datetime.now()}")
    
    # 1. 测试健康检查
    if not test_health_check():
        print("❌ 后端服务未正常运行，请检查服务状态")
        return
    
    print("✅ 后端服务正常")
    
    # 2. 测试爬虫配置
    if not test_crawler_config():
        print("❌ 爬虫配置测试失败")
        return
    
    print("✅ 爬虫配置正常")
    
    # 3. 测试获取所有任务
    test_get_all_tasks()
    
    # 4. 测试启动爬虫
    task_id = test_start_crawler()
    if not task_id:
        print("❌ 启动爬虫失败")
        return
    
    print(f"✅ 爬虫任务启动成功，任务ID: {task_id}")
    
    # 5. 监控爬虫进度
    final_status = monitor_crawler_progress(task_id, max_wait_time=120)
    
    # 6. 测试装备搜索
    search_result = test_equipment_search()
    
    # 7. 最终结果总结
    print("\n=== 测试结果总结 ===")
    if final_status:
        data = final_status.get('data', {})
        print(f"任务状态: {data.get('status')}")
        print(f"处理进度: {data.get('progress', 0)}%")
        print(f"成功数量: {data.get('success_count', 0)}")
        print(f"失败数量: {data.get('error_count', 0)}")
        
        if data.get('status') == 'completed':
            print("✅ 爬虫测试完全成功")
        elif data.get('status') == 'failed':
            print("❌ 爬虫任务失败")
            print(f"错误信息: {data.get('error_message', '未知错误')}")
        else:
            print("⚠️ 爬虫任务仍在进行中")
    else:
        print("❌ 无法获取最终状态")
    
    if search_result and search_result.get('success'):
        equipment_count = len(search_result.get('data', []))
        print(f"✅ 装备搜索成功，找到 {equipment_count} 条记录")
    else:
        print("❌ 装备搜索失败")
    
    print("\n测试完成！")

if __name__ == '__main__':
    main()