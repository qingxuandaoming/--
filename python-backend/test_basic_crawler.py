#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_basic_crawler():
    """测试基础爬虫功能"""
    base_url = "http://localhost:5000"
    
    print("=== 基础爬虫功能测试 ===")
    
    # 1. 健康检查
    print("\n1. 健康检查...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        print(f"健康检查状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ 后端服务正常")
        else:
            print("❌ 后端服务异常")
            return False
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False
    
    # 2. 启动爬虫任务
    print("\n2. 启动爬虫任务...")
    try:
        crawler_data = {
            "platform": "taobao",
            "category": "bike"
        }
        
        response = requests.post(
            f"{base_url}/api/crawler/start",
            json=crawler_data,
            timeout=30
        )
        
        print(f"启动爬虫状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                task_id = result.get('task_id')
                print(f"✅ 爬虫任务启动成功，任务ID: {task_id}")
                return task_id
            else:
                print(f"❌ 爬虫任务启动失败: {result.get('message')}")
                return False
        else:
            print(f"❌ 启动爬虫失败，状态码: {response.status_code}")
            print(f"错误响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 启动爬虫异常: {e}")
        return False

def test_crawler_status(task_id):
    """测试爬虫状态查询"""
    base_url = "http://localhost:5000"
    
    print(f"\n3. 查询爬虫任务状态 (任务ID: {task_id})...")
    try:
        response = requests.get(
            f"{base_url}/api/crawler/status/{task_id}",
            timeout=10
        )
        
        print(f"查询状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                status_data = result.get('data')
                print(f"✅ 任务状态查询成功: {status_data}")
                return True
            else:
                print(f"❌ 任务状态查询失败: {result.get('message')}")
                return False
        else:
            print(f"❌ 查询任务状态失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 查询任务状态异常: {e}")
        return False

if __name__ == "__main__":
    print("开始测试基础爬虫功能...")
    
    # 测试启动爬虫
    task_id = test_basic_crawler()
    
    if task_id:
        # 等待一下再查询状态
        time.sleep(2)
        
        # 测试状态查询
        test_crawler_status(task_id)
    
    print("\n测试完成！")