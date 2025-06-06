import requests
import time
import json
import uuid
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from loguru import logger
import threading
from concurrent.futures import ThreadPoolExecutor
import re
from urllib.parse import urljoin, urlparse

class CrawlerService:
    """爬虫服务类"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.tasks = {}  # 存储爬虫任务状态
        self.session = requests.Session()
        self._setup_session()
        
        # 骑行装备关键词分类
        self.equipment_categories = {
            'bike': ['自行车', '山地车', '公路车', '折叠车', '电动车'],
            'helmet': ['头盔', '骑行头盔', '安全帽'],
            'clothing': ['骑行服', '骑行裤', '骑行手套', '骑行鞋'],
            'accessories': ['车灯', '码表', '水壶', '车锁', '打气筒', '工具包'],
            'parts': ['轮胎', '内胎', '刹车片', '链条', '齿轮', '座垫']
        }
    
    def _setup_session(self):
        """设置请求会话"""
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def _get_webdriver(self, headless=True):
        """获取WebDriver实例"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(f'--user-agent={self.ua.random}')
        
        # 禁用图片加载以提高速度
        prefs = {
            "profile.managed_default_content_settings.images": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            logger.error(f"创建WebDriver失败: {str(e)}")
            return None
    
    def start_crawl_task(self, platform='all', category='all'):
        """启动爬虫任务"""
        task_id = str(uuid.uuid4())
        
        self.tasks[task_id] = {
            'id': task_id,
            'status': 'running',
            'platform': platform,
            'category': category,
            'start_time': datetime.now(),
            'progress': 0,
            'total_items': 0,
            'crawled_items': 0,
            'errors': [],
            'message': '任务启动中...'
        }
        
        # 在新线程中执行爬虫任务
        thread = threading.Thread(
            target=self._execute_crawl_task,
            args=(task_id, platform, category)
        )
        thread.daemon = True
        thread.start()
        
        return task_id
    
    def _execute_crawl_task(self, task_id, platform, category):
        """执行爬虫任务"""
        try:
            self.tasks[task_id]['message'] = '正在获取商品列表...'
            
            if platform == 'all' or platform == 'taobao':
                self._crawl_taobao(task_id, category)
            
            if platform == 'all' or platform == 'jd':
                self._crawl_jd(task_id, category)
            
            self.tasks[task_id]['status'] = 'completed'
            self.tasks[task_id]['message'] = '爬取任务完成'
            self.tasks[task_id]['end_time'] = datetime.now()
            
        except Exception as e:
            logger.error(f"爬虫任务执行失败: {str(e)}")
            self.tasks[task_id]['status'] = 'failed'
            self.tasks[task_id]['message'] = f'任务失败: {str(e)}'
            self.tasks[task_id]['errors'].append(str(e))
            self.tasks[task_id]['end_time'] = datetime.now()
    
    def _crawl_taobao(self, task_id, category):
        """爬取淘宝数据"""
        logger.info(f"开始爬取淘宝数据，分类: {category}")
        
        keywords = self._get_keywords_by_category(category)
        
        for keyword in keywords:
            try:
                self.tasks[task_id]['message'] = f'正在爬取淘宝: {keyword}'
                self._crawl_taobao_keyword(task_id, keyword)
                time.sleep(2)  # 避免请求过快
            except Exception as e:
                logger.error(f"爬取淘宝关键词 {keyword} 失败: {str(e)}")
                self.tasks[task_id]['errors'].append(f"淘宝-{keyword}: {str(e)}")
    
    def _crawl_taobao_keyword(self, task_id, keyword):
        """爬取淘宝特定关键词的商品"""
        # 淘宝搜索URL
        search_url = f"https://s.taobao.com/search?q={keyword}&sort=sale-desc"
        
        driver = self._get_webdriver()
        if not driver:
            raise Exception("无法创建WebDriver")
        
        try:
            driver.get(search_url)
            time.sleep(3)
            
            # 等待商品列表加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".item"))
            )
            
            # 获取商品列表
            items = driver.find_elements(By.CSS_SELECTOR, ".item")
            
            for i, item in enumerate(items[:20]):  # 限制每个关键词爬取20个商品
                try:
                    self._parse_taobao_item(task_id, item, keyword)
                    self.tasks[task_id]['crawled_items'] += 1
                    self.tasks[task_id]['progress'] = min(90, (i + 1) * 4)
                except Exception as e:
                    logger.error(f"解析淘宝商品失败: {str(e)}")
                    continue
        
        finally:
            driver.quit()
    
    def _parse_taobao_item(self, task_id, item_element, keyword):
        """解析淘宝商品信息"""
        try:
            # 商品标题
            title_elem = item_element.find_element(By.CSS_SELECTOR, ".title a")
            title = title_elem.get_attribute("title") or title_elem.text
            
            # 商品链接
            link = title_elem.get_attribute("href")
            if link and not link.startswith('http'):
                link = 'https:' + link
            
            # 价格
            price_elem = item_element.find_element(By.CSS_SELECTOR, ".price strong")
            price_text = price_elem.text.replace('¥', '').replace(',', '')
            price = float(re.findall(r'\d+\.?\d*', price_text)[0]) if re.findall(r'\d+\.?\d*', price_text) else 0
            
            # 商品图片
            img_elem = item_element.find_element(By.CSS_SELECTOR, ".pic img")
            image_url = img_elem.get_attribute("src") or img_elem.get_attribute("data-src")
            if image_url and not image_url.startswith('http'):
                image_url = 'https:' + image_url
            
            # 店铺信息
            shop_elem = item_element.find_element(By.CSS_SELECTOR, ".shop a")
            shop_name = shop_elem.text
            
            # 销量信息
            deal_cnt_elem = item_element.find_element(By.CSS_SELECTOR, ".deal-cnt")
            sales_text = deal_cnt_elem.text
            sales = self._extract_number(sales_text)
            
            # 保存商品信息
            equipment_data = {
                'name': title,
                'platform': 'taobao',
                'platform_url': link,
                'price': price,
                'image_url': image_url,
                'shop_name': shop_name,
                'sales': sales,
                'keyword': keyword,
                'crawl_time': datetime.now()
            }
            
            # 这里应该调用数据库保存方法
            self._save_equipment_data(equipment_data)
            
            logger.info(f"成功解析淘宝商品: {title}")
            
        except Exception as e:
            logger.error(f"解析淘宝商品元素失败: {str(e)}")
            raise
    
    def _crawl_jd(self, task_id, category):
        """爬取京东数据"""
        logger.info(f"开始爬取京东数据，分类: {category}")
        
        keywords = self._get_keywords_by_category(category)
        
        for keyword in keywords:
            try:
                self.tasks[task_id]['message'] = f'正在爬取京东: {keyword}'
                self._crawl_jd_keyword(task_id, keyword)
                time.sleep(2)
            except Exception as e:
                logger.error(f"爬取京东关键词 {keyword} 失败: {str(e)}")
                self.tasks[task_id]['errors'].append(f"京东-{keyword}: {str(e)}")
    
    def _crawl_jd_keyword(self, task_id, keyword):
        """爬取京东特定关键词的商品"""
        # 京东搜索URL
        search_url = f"https://search.jd.com/Search?keyword={keyword}&enc=utf-8&suggest=1.def.0.base&wq={keyword}&pvid=1"
        
        driver = self._get_webdriver()
        if not driver:
            raise Exception("无法创建WebDriver")
        
        try:
            driver.get(search_url)
            time.sleep(3)
            
            # 等待商品列表加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".gl-item"))
            )
            
            # 获取商品列表
            items = driver.find_elements(By.CSS_SELECTOR, ".gl-item")
            
            for i, item in enumerate(items[:20]):  # 限制每个关键词爬取20个商品
                try:
                    self._parse_jd_item(task_id, item, keyword)
                    self.tasks[task_id]['crawled_items'] += 1
                    self.tasks[task_id]['progress'] = min(90, (i + 1) * 4)
                except Exception as e:
                    logger.error(f"解析京东商品失败: {str(e)}")
                    continue
        
        finally:
            driver.quit()
    
    def _parse_jd_item(self, task_id, item_element, keyword):
        """解析京东商品信息"""
        try:
            # 商品标题
            title_elem = item_element.find_element(By.CSS_SELECTOR, ".p-name a em")
            title = title_elem.text
            
            # 商品链接
            link_elem = item_element.find_element(By.CSS_SELECTOR, ".p-name a")
            link = link_elem.get_attribute("href")
            if link and not link.startswith('http'):
                link = 'https:' + link
            
            # 价格
            price_elem = item_element.find_element(By.CSS_SELECTOR, ".p-price i")
            price_text = price_elem.text.replace('¥', '').replace(',', '')
            price = float(re.findall(r'\d+\.?\d*', price_text)[0]) if re.findall(r'\d+\.?\d*', price_text) else 0
            
            # 商品图片
            img_elem = item_element.find_element(By.CSS_SELECTOR, ".p-img img")
            image_url = img_elem.get_attribute("src") or img_elem.get_attribute("data-lazy-img")
            if image_url and not image_url.startswith('http'):
                image_url = 'https:' + image_url
            
            # 店铺信息
            try:
                shop_elem = item_element.find_element(By.CSS_SELECTOR, ".p-shop a")
                shop_name = shop_elem.text
            except:
                shop_name = "京东自营"
            
            # 评价数
            try:
                commit_elem = item_element.find_element(By.CSS_SELECTOR, ".p-commit a")
                commit_text = commit_elem.text
                commit_count = self._extract_number(commit_text)
            except:
                commit_count = 0
            
            # 保存商品信息
            equipment_data = {
                'name': title,
                'platform': 'jd',
                'platform_url': link,
                'price': price,
                'image_url': image_url,
                'shop_name': shop_name,
                'commit_count': commit_count,
                'keyword': keyword,
                'crawl_time': datetime.now()
            }
            
            # 这里应该调用数据库保存方法
            self._save_equipment_data(equipment_data)
            
            logger.info(f"成功解析京东商品: {title}")
            
        except Exception as e:
            logger.error(f"解析京东商品元素失败: {str(e)}")
            raise
    
    def _get_keywords_by_category(self, category):
        """根据分类获取关键词"""
        if category == 'all':
            keywords = []
            for cat_keywords in self.equipment_categories.values():
                keywords.extend(cat_keywords)
            return keywords
        elif category in self.equipment_categories:
            return self.equipment_categories[category]
        else:
            return [category]  # 如果是自定义分类，直接作为关键词
    
    def _extract_number(self, text):
        """从文本中提取数字"""
        numbers = re.findall(r'\d+', text.replace(',', ''))
        return int(numbers[0]) if numbers else 0
    
    def _save_equipment_data(self, data):
        """保存装备数据到数据库"""
        # 这里应该实现数据库保存逻辑
        # 暂时只记录日志
        logger.info(f"保存装备数据: {data['name']} - {data['platform']} - ¥{data['price']}")
    
    def get_task_status(self, task_id):
        """获取任务状态"""
        if task_id not in self.tasks:
            raise ValueError(f"任务 {task_id} 不存在")
        
        task = self.tasks[task_id].copy()
        
        # 计算运行时间
        if 'start_time' in task:
            if task['status'] == 'running':
                task['duration'] = (datetime.now() - task['start_time']).total_seconds()
            elif 'end_time' in task:
                task['duration'] = (task['end_time'] - task['start_time']).total_seconds()
        
        # 格式化时间
        if 'start_time' in task:
            task['start_time'] = task['start_time'].isoformat()
        if 'end_time' in task:
            task['end_time'] = task['end_time'].isoformat()
        
        return task
    
    def cleanup_old_tasks(self, days=7):
        """清理旧任务记录"""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        tasks_to_remove = []
        for task_id, task in self.tasks.items():
            if 'start_time' in task and task['start_time'] < cutoff_time:
                tasks_to_remove.append(task_id)
        
        for task_id in tasks_to_remove:
            del self.tasks[task_id]
        
        logger.info(f"清理了 {len(tasks_to_remove)} 个旧任务记录")