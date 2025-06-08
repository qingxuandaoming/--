#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新增API功能测试脚本
测试数据验证、推荐服务和价格预警API
"""

import requests
import json
import time
from datetime import datetime

# API基础URL
BASE_URL = 'http://localhost:5000/api'

def test_data_validation_apis():
    """测试数据验证API"""
    print("\n=== 测试数据验证API ===")
    
    # 测试单个装备数据验证
    print("\n1. 测试单个装备数据验证")
    test_equipment = {
        'name': '山地自行车 Giant ATX 830',
        'price': 2999.0,
        'platform': 'taobao',
        'link': 'https://item.taobao.com/item.htm?id=123456789',
        'image_url': 'https://img.alicdn.com/imgextra/i1/123456789.jpg',
        'shop_name': 'Giant官方旗舰店',
        'sales_count': 1500,
        'category': 'bike'
    }
    
    response = requests.post(f'{BASE_URL}/validation/validate', 
                           json={'equipment_data': test_equipment})
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 测试批量验证
    print("\n2. 测试批量装备数据验证")
    test_equipment_list = [
        test_equipment,
        {
            'name': '无效装备',  # 名称太短
            'price': -100,  # 价格无效
            'platform': 'invalid_platform',  # 平台无效
            'link': 'invalid_url',  # URL无效
            'category': 'bike'
        }
    ]
    
    response = requests.post(f'{BASE_URL}/validation/batch', 
                           json={'equipment_list': test_equipment_list})
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 测试验证摘要
    print("\n3. 测试获取验证摘要")
    response = requests.get(f'{BASE_URL}/validation/summary')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_recommendation_apis():
    """测试推荐服务API"""
    print("\n=== 测试推荐服务API ===")
    
    # 测试根据装备ID获取推荐
    print("\n1. 测试根据装备ID获取推荐")
    response = requests.get(f'{BASE_URL}/recommendations/equipment/1?limit=5')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 测试分类推荐
    print("\n2. 测试分类推荐")
    response = requests.get(f'{BASE_URL}/recommendations/category/bike?limit=5')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 测试价格区间推荐
    print("\n3. 测试价格区间推荐")
    response = requests.get(f'{BASE_URL}/recommendations/price-range?min_price=1000&max_price=5000&category=bike&limit=5')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 测试热门推荐
    print("\n4. 测试热门推荐")
    response = requests.get(f'{BASE_URL}/recommendations/trending?days=7&limit=5')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 测试推荐统计
    print("\n5. 测试推荐统计")
    response = requests.get(f'{BASE_URL}/recommendations/stats')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_price_alert_apis():
    """测试价格预警API"""
    print("\n=== 测试价格预警API ===")
    
    # 测试创建价格预警
    print("\n1. 测试创建价格预警")
    alert_data = {
        'equipment_id': 1,
        'alert_type': 'price_drop',
        'threshold_value': 10.0,
        'user_id': 'test_user_001',
        'email': 'test@example.com'
    }
    
    response = requests.post(f'{BASE_URL}/alerts', json=alert_data)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    alert_id = None
    if result.get('success') and 'data' in result:
        alert_id = result['data'].get('alert_id')
        print(f"创建的预警ID: {alert_id}")
    
    if alert_id:
        # 测试获取价格预警详情
        print("\n2. 测试获取价格预警详情")
        response = requests.get(f'{BASE_URL}/alerts/{alert_id}')
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        # 测试更新价格预警
        print("\n3. 测试更新价格预警")
        update_data = {
            'threshold_value': 15.0,
            'is_active': True
        }
        response = requests.put(f'{BASE_URL}/alerts/{alert_id}', json=update_data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 测试获取用户预警
    print("\n4. 测试获取用户预警")
    response = requests.get(f'{BASE_URL}/alerts/user/test_user_001')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 测试获取预警历史
    print("\n5. 测试获取预警历史")
    response = requests.get(f'{BASE_URL}/alerts/history?user_id=test_user_001&days=30')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 测试获取预警统计
    print("\n6. 测试获取预警统计")
    response = requests.get(f'{BASE_URL}/alerts/stats')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 测试启动价格监控
    print("\n7. 测试启动价格监控")
    response = requests.post(f'{BASE_URL}/alerts/start-monitoring')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 等待一段时间
    time.sleep(2)
    
    # 测试停止价格监控
    print("\n8. 测试停止价格监控")
    response = requests.post(f'{BASE_URL}/alerts/stop-monitoring')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    # 如果创建了预警，最后删除它
    if alert_id:
        print(f"\n9. 测试删除价格预警 (ID: {alert_id})")
        response = requests.delete(f'{BASE_URL}/alerts/{alert_id}')
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_health_check():
    """测试健康检查API"""
    print("\n=== 测试健康检查API ===")
    try:
        response = requests.get(f'{BASE_URL}/health', timeout=5)
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"健康检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print(f"开始测试新增API功能 - {datetime.now()}")
    print(f"API基础URL: {BASE_URL}")
    
    # 首先检查服务是否运行
    if not test_health_check():
        print("\n❌ 服务未运行，请先启动Flask应用")
        return
    
    print("\n✅ 服务运行正常，开始测试新增功能")
    
    try:
        # 测试数据验证API
        test_data_validation_apis()
        
        # 测试推荐服务API
        test_recommendation_apis()
        
        # 测试价格预警API
        test_price_alert_apis()
        
        print("\n🎉 所有API测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 连接失败，请确保Flask应用正在运行")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")

if __name__ == '__main__':
    main()