#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电商数据API集成测试脚本

使用说明：
1. 确保爬虫服务正在运行 (python app_crawler_test.py)
2. 配置API密钥后运行此脚本
3. 观察API和Selenium方式的效果对比
"""

import requests
import json
import time
from datetime import datetime

class APITester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health(self):
        """测试服务健康状态"""
        print("\n=== 测试服务健康状态 ===")
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 服务状态: {data['status']}")
                print(f"📅 时间戳: {data['timestamp']}")
                return True
            else:
                print(f"❌ 服务异常: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 连接失败: {str(e)}")
            return False
    
    def get_api_status(self):
        """获取API配置状态"""
        print("\n=== 获取API配置状态 ===")
        try:
            response = self.session.get(f"{self.base_url}/api/crawler/api-config")
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print("📊 API配置状态:")
                    for provider, status in data['data'].items():
                        enabled = "✅" if status['enabled'] else "❌"
                        configured = "✅" if status['configured'] else "❌"
                        print(f"  {provider}: 启用{enabled} 已配置{configured}")
                    return data['data']
                else:
                    print(f"❌ 获取失败: {data['message']}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 异常: {str(e)}")
        return None
    
    def configure_api(self, provider, app_key, app_secret=None):
        """配置API"""
        print(f"\n=== 配置{provider} API ===")
        try:
            payload = {
                "provider": provider,
                "app_key": app_key
            }
            if app_secret:
                payload["app_secret"] = app_secret
            
            response = self.session.post(
                f"{self.base_url}/api/crawler/api-config",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"✅ {data['message']}")
                    return True
                else:
                    print(f"❌ 配置失败: {data['message']}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 异常: {str(e)}")
        return False
    
    def get_crawl_methods(self):
        """获取爬取方式配置"""
        print("\n=== 获取爬取方式配置 ===")
        try:
            response = self.session.get(f"{self.base_url}/api/crawler/crawl-method")
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print("🔧 爬取方式配置:")
                    for method, enabled in data['data'].items():
                        status = "✅ 启用" if enabled else "❌ 禁用"
                        print(f"  {method}: {status}")
                    return data['data']
                else:
                    print(f"❌ 获取失败: {data['message']}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 异常: {str(e)}")
        return None
    
    def set_crawl_method(self, method, enabled):
        """设置爬取方式"""
        print(f"\n=== 设置{method}爬取方式 ===")
        try:
            payload = {
                "method": method,
                "enabled": enabled
            }
            
            response = self.session.put(
                f"{self.base_url}/api/crawler/crawl-method",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    action = "启用" if enabled else "禁用"
                    print(f"✅ 已{action}{method}爬取方式")
                    return True
                else:
                    print(f"❌ 设置失败: {data['message']}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 异常: {str(e)}")
        return False
    
    def start_crawler_task(self, platform="all", category="bike"):
        """启动爬虫任务"""
        print(f"\n=== 启动爬虫任务 ===")
        print(f"📋 平台: {platform}, 分类: {category}")
        try:
            payload = {
                "platform": platform,
                "category": category
            }
            
            response = self.session.post(
                f"{self.base_url}/api/crawler/start",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    task_id = data['task_id']
                    print(f"✅ 任务已启动")
                    print(f"🆔 任务ID: {task_id}")
                    return task_id
                else:
                    print(f"❌ 启动失败: {data['message']}")
            else:
                print(f"❌ 请求失败: {response.status_code}")
        except Exception as e:
            print(f"❌ 异常: {str(e)}")
        return None
    
    def monitor_task(self, task_id, max_wait_time=300):
        """监控任务执行"""
        print(f"\n=== 监控任务执行 ===")
        print(f"🆔 任务ID: {task_id}")
        
        start_time = time.time()
        last_status = None
        
        while time.time() - start_time < max_wait_time:
            try:
                response = self.session.get(f"{self.base_url}/api/crawler/status/{task_id}")
                if response.status_code == 200:
                    data = response.json()
                    if data['success']:
                        status_info = data['data']
                        current_status = status_info.get('status')
                        
                        # 只在状态变化时打印
                        if current_status != last_status:
                            print(f"📊 状态: {current_status}")
                            if 'message' in status_info:
                                print(f"💬 消息: {status_info['message']}")
                            if 'crawled_items' in status_info:
                                print(f"📦 已爬取: {status_info['crawled_items']} 个商品")
                            last_status = current_status
                        
                        if current_status in ['completed', 'failed']:
                            print(f"\n🏁 任务结束: {current_status}")
                            if 'errors' in status_info and status_info['errors']:
                                print("❌ 错误信息:")
                                for error in status_info['errors']:
                                    print(f"  - {error}")
                            return status_info
                    else:
                        print(f"❌ 获取状态失败: {data['message']}")
                        break
                else:
                    print(f"❌ 请求失败: {response.status_code}")
                    break
                
                time.sleep(5)  # 每5秒检查一次
                
            except Exception as e:
                print(f"❌ 监控异常: {str(e)}")
                break
        
        print(f"⏰ 监控超时 ({max_wait_time}秒)")
        return None
    
    def run_comprehensive_test(self):
        """运行综合测试"""
        print("🚀 开始电商数据API集成测试")
        print("=" * 50)
        
        # 1. 健康检查
        if not self.test_health():
            print("❌ 服务不可用，测试终止")
            return
        
        # 2. 检查当前配置
        api_status = self.get_api_status()
        crawl_methods = self.get_crawl_methods()
        
        # 3. 提示用户配置API（如果需要）
        if api_status:
            onebound_configured = api_status.get('onebound', {}).get('configured', False)
            if not onebound_configured:
                print("\n⚠️  万邦API未配置，将仅使用Selenium方式")
                print("💡 如需测试API方式，请先配置API密钥:")
                print("   tester.configure_api('onebound', 'your_app_key', 'your_app_secret')")
        
        # 4. 启动测试任务
        print("\n🎯 开始测试爬虫任务...")
        task_id = self.start_crawler_task(platform="taobao", category="bike")
        
        if task_id:
            # 5. 监控任务执行
            result = self.monitor_task(task_id)
            
            if result:
                print("\n📈 测试结果汇总:")
                print(f"  状态: {result.get('status', 'unknown')}")
                print(f"  爬取商品数: {result.get('crawled_items', 0)}")
                print(f"  开始时间: {result.get('start_time', 'unknown')}")
                print(f"  结束时间: {result.get('end_time', 'unknown')}")
                
                if result.get('status') == 'completed':
                    print("\n🎉 测试完成！API集成功能正常")
                else:
                    print("\n⚠️  测试未完全成功，请检查日志")
            else:
                print("\n❌ 无法获取最终结果")
        else:
            print("\n❌ 任务启动失败")
        
        print("\n" + "=" * 50)
        print("🏁 测试结束")

def main():
    """主函数"""
    tester = APITester()
    
    print("电商数据API集成测试工具")
    print("=" * 30)
    print("1. 运行综合测试")
    print("2. 配置万邦API")
    print("3. 查看当前状态")
    print("4. 设置爬取方式")
    print("0. 退出")
    
    while True:
        choice = input("\n请选择操作 (0-4): ").strip()
        
        if choice == "0":
            print("👋 再见！")
            break
        elif choice == "1":
            tester.run_comprehensive_test()
        elif choice == "2":
            app_key = input("请输入万邦API的app_key: ").strip()
            app_secret = input("请输入万邦API的app_secret: ").strip()
            if app_key and app_secret:
                tester.configure_api("onebound", app_key, app_secret)
            else:
                print("❌ 密钥不能为空")
        elif choice == "3":
            tester.get_api_status()
            tester.get_crawl_methods()
        elif choice == "4":
            print("可用的爬取方式: api, selenium, requests")
            method = input("请输入方式名称: ").strip()
            enabled_input = input("启用? (y/n): ").strip().lower()
            enabled = enabled_input in ['y', 'yes', '1', 'true']
            if method:
                tester.set_crawl_method(method, enabled)
            else:
                print("❌ 方式名称不能为空")
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()