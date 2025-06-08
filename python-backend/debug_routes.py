#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from app_crawler_test import app

def list_routes():
    """列出所有注册的路由"""
    print("=== Flask 应用路由列表 ===")
    
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
        print(f"{rule.endpoint:30s} {methods:20s} {rule.rule}")
    
    print("\n=== 路由总数:", len(list(app.url_map.iter_rules())))

def test_basic_endpoints():
    """测试基础端点"""
    print("\n=== 测试基础端点 ===")
    
    with app.test_client() as client:
        # 测试健康检查
        response = client.get('/api/health')
        print(f"健康检查: {response.status_code} - {response.get_json()}")
        
        # 测试爬虫启动
        response = client.post('/api/crawler/start', 
                             json={'platform': 'test', 'category': 'bike'})
        print(f"爬虫启动: {response.status_code} - {response.get_data(as_text=True)[:200]}")

if __name__ == "__main__":
    list_routes()
    test_basic_endpoints()