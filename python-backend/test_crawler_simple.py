#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_crawler_api():
    """测试爬虫API功能"""
    base_url = "http://127.0.0.1:5000"
    
    print("=== 爬虫功能测试 ===")
    
    # 1. 健康检查
    print("\n1. 健康检查...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✓ 服务正常运行")
            print(f"响应: {response.json()}")
        else:
            print(f"✗ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False
    
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
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                task_id = result.get('task_id')
                print(f"✓ 爬虫任务启动成功")
                print(f"任务ID: {task_id}")
                return task_id
            else:
                print(f"✗ 启动失败: {result.get('message')}")
                return False
        else:
            print(f"✗ 请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 启动爬虫失败: {e}")
        return False

def test_crawler_status(task_id):
    """测试爬虫状态查询"""
    base_url = "http://127.0.0.1:5000"
    
    print("\n3. 查询爬虫状态...")
    try:
        response = requests.get(f"{base_url}/api/crawler/status/{task_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"✓ 状态查询成功")
            print(f"任务状态: {result}")
            return True
        else:
            print(f"✗ 状态查询失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"✗ 查询状态失败: {e}")
        return False

def main():
    """主测试函数"""
    # 启动爬虫任务
    task_id = test_crawler_api()
    
    if task_id:
        # 等待一段时间后查询状态
        time.sleep(2)
        test_crawler_status(task_id)
        
        # 再次查询状态
        time.sleep(3)
        test_crawler_status(task_id)
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()