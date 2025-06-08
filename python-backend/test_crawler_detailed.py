#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_crawler_functionality():
    """详细测试爬虫功能"""
    base_url = "http://127.0.0.1:5000"
    
    print("=== 详细爬虫功能测试 ===")
    
    # 1. 健康检查
    print("\n1. 健康检查...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"✓ 服务正常: {health_data}")
        else:
            print(f"✗ 健康检查失败")
            return
    except Exception as e:
        print(f"✗ 健康检查异常: {e}")
        return
    
    # 2. 启动爬虫任务
    print("\n2. 启动爬虫任务...")
    try:
        payload = {
            "platform": "test",
            "category": "bike"
        }
        
        response = requests.post(
            f"{base_url}/api/crawler/start",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success'):
                    task_id = result.get('task_id')
                    print(f"✓ 爬虫任务启动成功，任务ID: {task_id}")
                    return task_id
                else:
                    print(f"✗ 启动失败: {result.get('message')}")
            except json.JSONDecodeError as e:
                print(f"✗ JSON解析失败: {e}")
                print(f"原始响应: {response.text}")
        else:
            print(f"✗ 请求失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"✗ 启动爬虫异常: {e}")
    
    return None

def test_crawler_status(task_id):
    """测试爬虫状态查询"""
    base_url = "http://127.0.0.1:5000"
    
    print(f"\n3. 查询爬虫状态 (任务ID: {task_id})...")
    try:
        response = requests.get(f"{base_url}/api/crawler/status/{task_id}")
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✓ 状态查询成功")
                print(f"任务状态: {json.dumps(result, indent=2, ensure_ascii=False)}")
                return result
            except json.JSONDecodeError as e:
                print(f"✗ JSON解析失败: {e}")
        else:
            print(f"✗ 状态查询失败")
            
    except Exception as e:
        print(f"✗ 查询状态异常: {e}")
    
    return None

def main():
    """主测试函数"""
    # 启动爬虫任务
    task_id = test_crawler_functionality()
    
    if task_id:
        # 等待一段时间后查询状态
        print("\n等待2秒后查询状态...")
        time.sleep(2)
        status1 = test_crawler_status(task_id)
        
        # 再次查询状态
        print("\n再等待3秒后查询状态...")
        time.sleep(3)
        status2 = test_crawler_status(task_id)
        
        # 分析状态变化
        if status1 and status2:
            print("\n=== 状态变化分析 ===")
            data1 = status1.get('data', {})
            data2 = status2.get('data', {})
            
            print(f"第一次查询状态: {data1.get('status', 'unknown')}")
            print(f"第二次查询状态: {data2.get('status', 'unknown')}")
            print(f"进度变化: {data1.get('progress', 0)} -> {data2.get('progress', 0)}")
            print(f"爬取数量: {data2.get('crawled_items', 0)}")
            
            if data2.get('errors'):
                print(f"错误信息: {data2.get('errors')}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()