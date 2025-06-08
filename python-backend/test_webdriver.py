#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WebDriver测试脚本
测试Selenium WebDriver是否能正常工作
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from loguru import logger
import time

def test_webdriver():
    """测试WebDriver"""
    print("开始测试WebDriver...")
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # 反检测配置
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        print("正在下载/配置ChromeDriver...")
        # 使用webdriver-manager自动管理ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("WebDriver创建成功！")
        
        # 测试访问一个简单的网页
        print("测试访问百度首页...")
        driver.get("https://www.baidu.com")
        
        # 获取页面标题
        title = driver.title
        print(f"页面标题: {title}")
        
        # 等待一下
        time.sleep(2)
        
        # 关闭浏览器
        driver.quit()
        print("WebDriver测试成功完成！")
        return True
        
    except Exception as e:
        print(f"WebDriver测试失败: {str(e)}")
        logger.error(f"WebDriver测试失败: {str(e)}")
        return False

def test_jd_access():
    """测试访问京东"""
    print("\n开始测试访问京东...")
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 测试访问京东搜索页面
        search_url = "https://search.jd.com/Search?keyword=自行车&enc=utf-8"
        print(f"访问URL: {search_url}")
        
        driver.get(search_url)
        time.sleep(3)
        
        title = driver.title
        print(f"京东页面标题: {title}")
        
        # 检查页面是否正常加载
        page_source = driver.page_source
        if "自行车" in page_source or "商品" in page_source:
            print("京东页面加载成功，包含预期内容")
            result = True
        else:
            print("京东页面可能被反爬虫拦截")
            result = False
        
        driver.quit()
        return result
        
    except Exception as e:
        print(f"访问京东失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("WebDriver功能测试")
    print("=" * 50)
    
    # 测试基础WebDriver功能
    basic_test = test_webdriver()
    
    # 测试访问京东
    jd_test = test_jd_access()
    
    print("\n=" * 50)
    print("测试结果汇总:")
    print(f"基础WebDriver测试: {'成功' if basic_test else '失败'}")
    print(f"京东访问测试: {'成功' if jd_test else '失败'}")
    print("=" * 50)
    
    return basic_test and jd_test

if __name__ == "__main__":
    main()