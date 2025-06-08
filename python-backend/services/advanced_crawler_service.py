# -*- coding: utf-8 -*-
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
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from urllib.parse import urljoin, urlparse
import random
from typing import Dict, List, Optional, Tuple

class AdvancedCrawlerService:
    """高级爬虫服务类"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.tasks = {}  # 存储爬虫任务状态
        self.session = requests.Session()
        self._setup_session()
        
        # 反反爬配置
        self.request_delay = (2, 5)  # 请求间隔范围（秒）
        self.max_retries = 3  # 最大重试次数
        self.timeout = 30  # 请求超时时间
        self.max_workers = 3  # 最大并发数
        
        # 代理池配置
        self.proxy_pool = []
        self.current_proxy_index = 0
        
        # 支持的平台配置
        self.platforms = {
            'taobao': {
                'name': '淘宝',
                'search_url': 'https://s.taobao.com/search?q={keyword}&sort=sale-desc',
                'selectors': {
                    'items': '.item',
                    'title': '.title a',
                    'price': '.price strong',
                    'image': '.pic img',
                    'shop': '.shop a',
                    'sales': '.deal-cnt'
                }
            },
            'jd': {
                'name': '京东',
                'search_url': 'https://search.jd.com/Search?keyword={keyword}&enc=utf-8',
                'selectors': {
                    'items': '.gl-item',
                    'title': '.p-name a em',
                    'price': '.p-price i',
                    'image': '.p-img img',
                    'shop': '.p-shop a',
                    'sales': '.p-commit a'
                }
            },
            'tmall': {
                'name': '天猫',
                'search_url': 'https://list.tmall.com/search_product.htm?q={keyword}&sort=s&style=g',
                'selectors': {
                    'items': '.product',
                    'title': '.productTitle a',
                    'price': '.productPrice em',
                    'image': '.productImg img',
                    'shop': '.productShop a',
                    'sales': '.productStatus span'
                }
            }
        }
        
        # 骑行装备关键词分类（扩展版）
        self.equipment_categories = {
            'bike': {
                'keywords': ['自行车', '山地车', '公路车', '折叠车', '电动车', '单车', 'bike', 'bicycle'],
                'subcategories': ['山地车', '公路车', '折叠车', '电动车', '城市车', '儿童车']
            },
            'helmet': {
                'keywords': ['头盔', '骑行头盔', '安全帽', 'helmet', '防护帽'],
                'subcategories': ['山地头盔', '公路头盔', '城市头盔', '儿童头盔']
            },
            'clothing': {
                'keywords': ['骑行服', '骑行裤', '骑行手套', '骑行鞋', '骑行袜', 'jersey', 'shorts'],
                'subcategories': ['骑行上衣', '骑行裤', '骑行手套', '骑行鞋', '骑行袜子']
            },
            'accessories': {
                'keywords': ['车灯', '码表', '水壶', '车锁', '打气筒', '工具包', 'light', 'computer'],
                'subcategories': ['车灯', '码表', '水壶架', '车锁', '打气筒', '维修工具']
            },
            'parts': {
                'keywords': ['轮胎', '内胎', '刹车片', '链条', '齿轮', '座垫', 'tire', 'brake'],
                'subcategories': ['轮胎', '内胎', '刹车系统', '传动系统', '座垫', '把手']
            },
            'safety': {
                'keywords': ['护膝', '护肘', '反光衣', '尾灯', '铃铛'],
                'subcategories': ['护具', '反光装备', '警示装备']
            }
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
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'DNT': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        })
        self.session.timeout = self.timeout
    
    def start_advanced_crawl_task(self, platforms: List[str] = None, categories: List[str] = None, 
                                 keywords: List[str] = None, max_items_per_keyword: int = 50):
        """启动高级爬虫任务"""
        task_id = str(uuid.uuid4())
        
        # 默认参数
        if platforms is None:
            platforms = ['taobao', 'jd']
        if categories is None:
            categories = ['bike', 'helmet', 'clothing', 'accessories']
        
        self.tasks[task_id] = {
            'id': task_id,
            'status': 'running',
            'platforms': platforms,
            'categories': categories,
            'keywords': keywords,
            'max_items_per_keyword': max_items_per_keyword,
            'start_time': datetime.now(),
            'progress': 0,
            'total_items': 0,
            'crawled_items': 0,
            'success_items': 0,
            'failed_items': 0,
            'errors': [],
            'message': '任务启动中...',
            'platform_stats': {}
        }
        
        # 在新线程中执行爬虫任务
        thread = threading.Thread(
            target=self._execute_advanced_crawl_task,
            args=(task_id, platforms, categories, keywords, max_items_per_keyword)
        )
        thread.daemon = True
        thread.start()
        
        return task_id
    
    def _execute_advanced_crawl_task(self, task_id: str, platforms: List[str], 
                                   categories: List[str], keywords: List[str], 
                                   max_items_per_keyword: int):
        """执行高级爬虫任务"""
        try:
            self.tasks[task_id]['message'] = '正在准备爬虫任务...'
            
            # 生成关键词列表
            if keywords is None:
                keywords = self._generate_keywords_from_categories(categories)
            
            total_tasks = len(platforms) * len(keywords)
            self.tasks[task_id]['total_tasks'] = total_tasks
            completed_tasks = 0
            
            # 使用线程池并发爬取
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = []
                
                for platform in platforms:
                    if platform not in self.platforms:
                        logger.warning(f"不支持的平台: {platform}")
                        continue
                    
                    self.tasks[task_id]['platform_stats'][platform] = {
                        'total_keywords': len(keywords),
                        'completed_keywords': 0,
                        'success_items': 0,
                        'failed_items': 0
                    }
                    
                    for keyword in keywords:
                        future = executor.submit(
                            self._crawl_platform_keyword,
                            task_id, platform, keyword, max_items_per_keyword
                        )
                        futures.append((future, platform, keyword))
                
                # 处理完成的任务
                for future, platform, keyword in as_completed([(f[0], f[1], f[2]) for f in futures]):
                    try:
                        result = future.result()
                        completed_tasks += 1
                        
                        # 更新统计信息
                        self.tasks[task_id]['platform_stats'][platform]['completed_keywords'] += 1
                        self.tasks[task_id]['platform_stats'][platform]['success_items'] += result.get('success', 0)
                        self.tasks[task_id]['platform_stats'][platform]['failed_items'] += result.get('failed', 0)
                        
                        self.tasks[task_id]['success_items'] += result.get('success', 0)
                        self.tasks[task_id]['failed_items'] += result.get('failed', 0)
                        self.tasks[task_id]['crawled_items'] += result.get('total', 0)
                        
                        # 更新进度
                        progress = int((completed_tasks / total_tasks) * 100)
                        self.tasks[task_id]['progress'] = progress
                        self.tasks[task_id]['message'] = f'已完成 {completed_tasks}/{total_tasks} 个爬取任务'
                        
                        logger.info(f"完成爬取: {platform} - {keyword}, 成功: {result.get('success', 0)}, 失败: {result.get('failed', 0)}")
                        
                    except Exception as e:
                        logger.error(f"爬取任务失败: {platform} - {keyword}: {str(e)}")
                        self.tasks[task_id]['errors'].append(f"{platform}-{keyword}: {str(e)}")
                        completed_tasks += 1
            
            self.tasks[task_id]['status'] = 'completed'
            self.tasks[task_id]['message'] = '爬取任务完成'
            self.tasks[task_id]['end_time'] = datetime.now()
            self.tasks[task_id]['progress'] = 100
            
            logger.info(f"高级爬虫任务完成: {task_id}, 总计爬取: {self.tasks[task_id]['crawled_items']} 个商品")
            
        except Exception as e:
            logger.error(f"高级爬虫任务执行失败: {str(e)}")
            self.tasks[task_id]['status'] = 'failed'
            self.tasks[task_id]['message'] = f'任务失败: {str(e)}'
            self.tasks[task_id]['errors'].append(str(e))
            self.tasks[task_id]['end_time'] = datetime.now()
    
    def _generate_keywords_from_categories(self, categories: List[str]) -> List[str]:
        """从分类生成关键词"""
        keywords = []
        for category in categories:
            if category in self.equipment_categories:
                keywords.extend(self.equipment_categories[category]['keywords'])
        return list(set(keywords))  # 去重
    
    def _crawl_platform_keyword(self, task_id: str, platform: str, keyword: str, max_items: int) -> Dict:
        """爬取特定平台的关键词"""
        success_count = 0
        failed_count = 0
        
        try:
            logger.info(f"开始爬取: {platform} - {keyword}")
            
            if platform == 'taobao':
                result = self._crawl_taobao_advanced(task_id, keyword, max_items)
            elif platform == 'jd':
                result = self._crawl_jd_advanced(task_id, keyword, max_items)
            elif platform == 'tmall':
                result = self._crawl_tmall_advanced(task_id, keyword, max_items)
            else:
                raise ValueError(f"不支持的平台: {platform}")
            
            success_count = result.get('success', 0)
            failed_count = result.get('failed', 0)
            
        except Exception as e:
            logger.error(f"爬取平台关键词失败: {platform} - {keyword}: {str(e)}")
            failed_count = 1
        
        return {
            'success': success_count,
            'failed': failed_count,
            'total': success_count + failed_count
        }
    
    def _crawl_taobao_advanced(self, task_id: str, keyword: str, max_items: int) -> Dict:
        """高级淘宝爬虫"""
        success_count = 0
        failed_count = 0
        
        driver = self._get_advanced_webdriver()
        if not driver:
            raise Exception("无法创建WebDriver")
        
        try:
            search_url = self.platforms['taobao']['search_url'].format(keyword=keyword)
            driver.get(search_url)
            
            # 等待页面加载
            time.sleep(random.uniform(3, 6))
            
            # 滚动页面加载更多商品
            self._scroll_page(driver, max_scrolls=3)
            
            # 获取商品列表
            items = driver.find_elements(By.CSS_SELECTOR, self.platforms['taobao']['selectors']['items'])
            
            for i, item in enumerate(items[:max_items]):
                try:
                    equipment_data = self._parse_taobao_item_advanced(item, keyword)
                    if equipment_data:
                        self._save_equipment_data_advanced(equipment_data)
                        success_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    logger.error(f"解析淘宝商品失败: {str(e)}")
                    failed_count += 1
                
                # 添加随机延迟
                if i % 5 == 0:
                    time.sleep(random.uniform(1, 2))
        
        finally:
            driver.quit()
        
        return {'success': success_count, 'failed': failed_count}
    
    def _crawl_jd_advanced(self, task_id: str, keyword: str, max_items: int) -> Dict:
        """高级京东爬虫"""
        success_count = 0
        failed_count = 0
        
        driver = self._get_advanced_webdriver()
        if not driver:
            raise Exception("无法创建WebDriver")
        
        try:
            search_url = self.platforms['jd']['search_url'].format(keyword=keyword)
            driver.get(search_url)
            
            # 等待页面加载
            time.sleep(random.uniform(3, 6))
            
            # 滚动页面加载更多商品
            self._scroll_page(driver, max_scrolls=3)
            
            # 获取商品列表
            items = driver.find_elements(By.CSS_SELECTOR, self.platforms['jd']['selectors']['items'])
            
            for i, item in enumerate(items[:max_items]):
                try:
                    equipment_data = self._parse_jd_item_advanced(item, keyword)
                    if equipment_data:
                        self._save_equipment_data_advanced(equipment_data)
                        success_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    logger.error(f"解析京东商品失败: {str(e)}")
                    failed_count += 1
                
                # 添加随机延迟
                if i % 5 == 0:
                    time.sleep(random.uniform(1, 2))
        
        finally:
            driver.quit()
        
        return {'success': success_count, 'failed': failed_count}
    
    def _crawl_tmall_advanced(self, task_id: str, keyword: str, max_items: int) -> Dict:
        """高级天猫爬虫"""
        success_count = 0
        failed_count = 0
        
        driver = self._get_advanced_webdriver()
        if not driver:
            raise Exception("无法创建WebDriver")
        
        try:
            search_url = self.platforms['tmall']['search_url'].format(keyword=keyword)
            driver.get(search_url)
            
            # 等待页面加载
            time.sleep(random.uniform(3, 6))
            
            # 滚动页面加载更多商品
            self._scroll_page(driver, max_scrolls=3)
            
            # 获取商品列表
            items = driver.find_elements(By.CSS_SELECTOR, self.platforms['tmall']['selectors']['items'])
            
            for i, item in enumerate(items[:max_items]):
                try:
                    equipment_data = self._parse_tmall_item_advanced(item, keyword)
                    if equipment_data:
                        self._save_equipment_data_advanced(equipment_data)
                        success_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    logger.error(f"解析天猫商品失败: {str(e)}")
                    failed_count += 1
                
                # 添加随机延迟
                if i % 5 == 0:
                    time.sleep(random.uniform(1, 2))
        
        finally:
            driver.quit()
        
        return {'success': success_count, 'failed': failed_count}
    
    def _get_advanced_webdriver(self, headless: bool = True) -> Optional[webdriver.Chrome]:
        """获取高级WebDriver实例"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless')
        
        # 基础配置
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(f'--user-agent={self.ua.random}')
        
        # 高级反检测配置
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        
        # 性能优化
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values": {
                "notifications": 2,
                "media_stream": 2,
                "geolocation": 2,
                "camera": 2,
                "microphone": 2
            },
            "profile.managed_default_content_settings.media_stream": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            
            # 执行高级反检测脚本
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']})")
            driver.execute_script("Object.defineProperty(navigator, 'platform', {get: () => 'Win32'})")
            
            # 设置超时
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
            return driver
        except Exception as e:
            logger.error(f"创建高级WebDriver失败: {str(e)}")
            return None
    
    def _scroll_page(self, driver: webdriver.Chrome, max_scrolls: int = 3):
        """滚动页面加载更多内容"""
        for i in range(max_scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 4))
    
    def _parse_taobao_item_advanced(self, item_element, keyword: str) -> Optional[Dict]:
        """高级解析淘宝商品信息"""
        try:
            selectors = self.platforms['taobao']['selectors']
            
            # 商品标题
            title_elem = item_element.find_element(By.CSS_SELECTOR, selectors['title'])
            title = title_elem.get_attribute("title") or title_elem.text
            
            if not title or len(title.strip()) < 5:
                return None
            
            # 商品链接
            link = title_elem.get_attribute("href")
            if link and not link.startswith('http'):
                link = 'https:' + link
            
            # 价格
            try:
                price_elem = item_element.find_element(By.CSS_SELECTOR, selectors['price'])
                price_text = price_elem.text.replace('¥', '').replace(',', '')
                price = float(re.findall(r'\d+\.?\d*', price_text)[0]) if re.findall(r'\d+\.?\d*', price_text) else 0
            except:
                price = 0
            
            # 商品图片
            try:
                img_elem = item_element.find_element(By.CSS_SELECTOR, selectors['image'])
                image_url = img_elem.get_attribute("src") or img_elem.get_attribute("data-src")
                if image_url and not image_url.startswith('http'):
                    image_url = 'https:' + image_url
            except:
                image_url = ''
            
            # 店铺信息
            try:
                shop_elem = item_element.find_element(By.CSS_SELECTOR, selectors['shop'])
                shop_name = shop_elem.text
            except:
                shop_name = ''
            
            # 销量信息
            try:
                sales_elem = item_element.find_element(By.CSS_SELECTOR, selectors['sales'])
                sales_text = sales_elem.text
                sales = self._extract_number(sales_text)
            except:
                sales = 0
            
            return {
                'name': title.strip(),
                'platform': 'taobao',
                'platform_url': link,
                'price': price,
                'image_url': image_url,
                'shop_name': shop_name.strip() if shop_name else '',
                'sales': sales,
                'keyword': keyword,
                'crawl_time': datetime.now(),
                'source': 'advanced_crawler'
            }
            
        except Exception as e:
            logger.error(f"解析淘宝商品失败: {str(e)}")
            return None
    
    def _parse_jd_item_advanced(self, item_element, keyword: str) -> Optional[Dict]:
        """高级解析京东商品信息"""
        try:
            selectors = self.platforms['jd']['selectors']
            
            # 商品标题
            title_elem = item_element.find_element(By.CSS_SELECTOR, selectors['title'])
            title = title_elem.text
            
            if not title or len(title.strip()) < 5:
                return None
            
            # 商品链接
            try:
                link_elem = item_element.find_element(By.CSS_SELECTOR, '.p-name a')
                link = link_elem.get_attribute("href")
                if link and not link.startswith('http'):
                    link = 'https:' + link
            except:
                link = ''
            
            # 价格
            try:
                price_elem = item_element.find_element(By.CSS_SELECTOR, selectors['price'])
                price_text = price_elem.text.replace('¥', '').replace(',', '')
                price = float(re.findall(r'\d+\.?\d*', price_text)[0]) if re.findall(r'\d+\.?\d*', price_text) else 0
            except:
                price = 0
            
            # 商品图片
            try:
                img_elem = item_element.find_element(By.CSS_SELECTOR, selectors['image'])
                image_url = img_elem.get_attribute("src") or img_elem.get_attribute("data-lazy-img")
                if image_url and not image_url.startswith('http'):
                    image_url = 'https:' + image_url
            except:
                image_url = ''
            
            # 店铺信息
            try:
                shop_elem = item_element.find_element(By.CSS_SELECTOR, selectors['shop'])
                shop_name = shop_elem.text
            except:
                shop_name = "京东自营"
            
            # 评价数
            try:
                commit_elem = item_element.find_element(By.CSS_SELECTOR, selectors['sales'])
                commit_text = commit_elem.text
                commit_count = self._extract_number(commit_text)
            except:
                commit_count = 0
            
            return {
                'name': title.strip(),
                'platform': 'jd',
                'platform_url': link,
                'price': price,
                'image_url': image_url,
                'shop_name': shop_name.strip() if shop_name else '',
                'commit_count': commit_count,
                'keyword': keyword,
                'crawl_time': datetime.now(),
                'source': 'advanced_crawler'
            }
            
        except Exception as e:
            logger.error(f"解析京东商品失败: {str(e)}")
            return None
    
    def _parse_tmall_item_advanced(self, item_element, keyword: str) -> Optional[Dict]:
        """高级解析天猫商品信息"""
        try:
            selectors = self.platforms['tmall']['selectors']
            
            # 商品标题
            title_elem = item_element.find_element(By.CSS_SELECTOR, selectors['title'])
            title = title_elem.text
            
            if not title or len(title.strip()) < 5:
                return None
            
            # 商品链接
            link = title_elem.get_attribute("href")
            if link and not link.startswith('http'):
                link = 'https:' + link
            
            # 价格
            try:
                price_elem = item_element.find_element(By.CSS_SELECTOR, selectors['price'])
                price_text = price_elem.text.replace('¥', '').replace(',', '')
                price = float(re.findall(r'\d+\.?\d*', price_text)[0]) if re.findall(r'\d+\.?\d*', price_text) else 0
            except:
                price = 0
            
            # 商品图片
            try:
                img_elem = item_element.find_element(By.CSS_SELECTOR, selectors['image'])
                image_url = img_elem.get_attribute("src") or img_elem.get_attribute("data-src")
                if image_url and not image_url.startswith('http'):
                    image_url = 'https:' + image_url
            except:
                image_url = ''
            
            # 店铺信息
            try:
                shop_elem = item_element.find_element(By.CSS_SELECTOR, selectors['shop'])
                shop_name = shop_elem.text
            except:
                shop_name = ''
            
            return {
                'name': title.strip(),
                'platform': 'tmall',
                'platform_url': link,
                'price': price,
                'image_url': image_url,
                'shop_name': shop_name.strip() if shop_name else '',
                'keyword': keyword,
                'crawl_time': datetime.now(),
                'source': 'advanced_crawler'
            }
            
        except Exception as e:
            logger.error(f"解析天猫商品失败: {str(e)}")
            return None
    
    def _extract_number(self, text: str) -> int:
        """从文本中提取数字"""
        numbers = re.findall(r'\d+', text.replace(',', ''))
        return int(numbers[0]) if numbers else 0
    
    def _save_equipment_data_advanced(self, data: Dict):
        """保存装备数据到数据库（高级版）"""
        try:
            from app import db, Equipment, EquipmentPrice, EquipmentCategory
            
            # 数据清洗和验证
            cleaned_data = self._clean_equipment_data_advanced(data)
            
            if not self._validate_equipment_data(cleaned_data):
                logger.warning(f"数据验证失败，跳过保存: {cleaned_data.get('name', 'Unknown')}")
                return False
            
            # 检查是否已存在相同商品
            existing_equipment = Equipment.query.filter(
                Equipment.name == cleaned_data['name'],
                Equipment.platform_url == cleaned_data.get('platform_url')
            ).first()
            
            if existing_equipment:
                # 更新现有商品信息
                existing_equipment.price = cleaned_data['price']
                existing_equipment.updated_at = datetime.now()
                equipment_id = existing_equipment.id
                logger.debug(f"更新现有装备: {cleaned_data['name']}")
            else:
                # 创建新商品
                equipment = Equipment(
                    name=cleaned_data['name'],
                    brand=self._extract_brand(cleaned_data['name']),
                    category=self._classify_equipment_advanced(cleaned_data['name'], cleaned_data.get('keyword', '')),
                    price=cleaned_data['price'],
                    description=cleaned_data.get('description', ''),
                    image_urls=[cleaned_data.get('image_url')] if cleaned_data.get('image_url') else [],
                    purchase_urls=[{
                        'platform': cleaned_data['platform'],
                        'url': cleaned_data.get('platform_url', ''),
                        'shop_name': cleaned_data.get('shop_name', '')
                    }],
                    rating_count=cleaned_data.get('sales', 0),
                    platform_url=cleaned_data.get('platform_url', ''),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.session.add(equipment)
                db.session.flush()  # 获取ID
                equipment_id = equipment.id
                logger.debug(f"创建新装备: {cleaned_data['name']}")
            
            # 保存价格历史
            price_record = EquipmentPrice(
                equipment_id=equipment_id,
                platform=cleaned_data['platform'],
                price=cleaned_data['price'],
                currency='CNY',
                shop_name=cleaned_data.get('shop_name', ''),
                shop_url=cleaned_data.get('shop_url', ''),
                is_available=True,
                recorded_at=datetime.now()
            )
            db.session.add(price_record)
            
            db.session.commit()
            logger.info(f"成功保存装备数据: {cleaned_data['name']} - {cleaned_data['platform']} - ¥{cleaned_data['price']}")
            return True
            
        except Exception as e:
            logger.error(f"保存装备数据失败: {str(e)}")
            if 'db' in locals():
                db.session.rollback()
            return False
    
    def _clean_equipment_data_advanced(self, data: Dict) -> Dict:
        """高级数据清洗"""
        cleaned = data.copy()
        
        # 清洗商品名称
        if 'name' in cleaned:
            name = cleaned['name']
            # 移除多余的空格和特殊字符
            name = re.sub(r'\s+', ' ', name).strip()
            # 移除HTML标签
            name = re.sub(r'<[^>]+>', '', name)
            # 移除特殊符号
            name = re.sub(r'[\u2600-\u26FF\u2700-\u27BF]', '', name)  # 移除emoji
            # 限制长度
            cleaned['name'] = name[:200] if name else ''
        
        # 清洗价格
        if 'price' in cleaned:
            price = cleaned['price']
            if isinstance(price, str):
                # 提取数字
                price_match = re.search(r'\d+\.?\d*', price.replace(',', ''))
                cleaned['price'] = float(price_match.group()) if price_match else 0.0
            elif price is None:
                cleaned['price'] = 0.0
            
            # 价格合理性检查
            if cleaned['price'] > 100000:  # 价格过高，可能是错误数据
                cleaned['price'] = 0.0
        
        # 清洗图片URL
        if 'image_url' in cleaned and cleaned['image_url']:
            image_url = cleaned['image_url']
            if not image_url.startswith('http'):
                if image_url.startswith('//'):
                    cleaned['image_url'] = 'https:' + image_url
                elif image_url.startswith('/'):
                    if 'taobao' in cleaned.get('platform', ''):
                        cleaned['image_url'] = 'https://img.alicdn.com' + image_url
                    elif 'jd' in cleaned.get('platform', ''):
                        cleaned['image_url'] = 'https://img.jd.com' + image_url
        
        # 清洗店铺名称
        if 'shop_name' in cleaned:
            shop_name = cleaned['shop_name']
            if shop_name:
                shop_name = re.sub(r'\s+', ' ', shop_name).strip()
                cleaned['shop_name'] = shop_name[:100]
        
        return cleaned
    
    def _validate_equipment_data(self, data: Dict) -> bool:
        """验证装备数据"""
        # 必须有商品名称
        if not data.get('name') or len(data['name'].strip()) < 3:
            return False
        
        # 价格必须大于0
        if data.get('price', 0) <= 0:
            return False
        
        # 必须有平台信息
        if not data.get('platform'):
            return False
        
        return True
    
    def _extract_brand(self, name: str) -> str:
        """从商品名称中提取品牌"""
        # 常见骑行装备品牌
        brands = [
            'Giant', '捷安特', 'Trek', 'Specialized', 'Cannondale', 'Scott', 'Merida', '美利达',
            'Shimano', '禧玛诺', 'SRAM', 'Campagnolo', 'Mavic', 'Continental', '马牌',
            'Schwalbe', 'Michelin', '米其林', 'Kenda', '建大', 'Maxxis', '玛吉斯',
            'Pearl Izumi', 'Castelli', 'Rapha', 'Assos', 'Endura', 'Gore', 'Giro',
            'Bell', 'Kask', 'POC', 'Smith', 'Oakley', 'Rudy Project'
        ]
        
        name_upper = name.upper()
        for brand in brands:
            if brand.upper() in name_upper:
                return brand
        
        # 如果没有找到已知品牌，尝试提取第一个单词作为品牌
        words = name.split()
        if words:
            first_word = words[0]
            if len(first_word) > 1 and first_word.isalpha():
                return first_word
        
        return ''
    
    def _classify_equipment_advanced(self, name: str, keyword: str = '') -> str:
        """高级装备分类"""
        name_lower = name.lower()
        keyword_lower = keyword.lower()
        text = f"{name_lower} {keyword_lower}"
        
        # 更详细的分类规则
        classification_rules = {
            '自行车': [
                ['自行车', '单车', 'bike', 'bicycle', '车架', 'frame'],
                ['山地车', 'mtb', 'mountain'],
                ['公路车', 'road', '公路'],
                ['折叠车', 'folding', '折叠'],
                ['电动车', 'electric', 'e-bike', '电动']
            ],
            '安全防护': [
                ['头盔', 'helmet', '安全帽'],
                ['护膝', '护肘', '护具', 'pad', 'protection'],
                ['反光', 'reflective', '警示']
            ],
            '骑行服装': [
                ['骑行服', 'jersey', '上衣', '短袖', '长袖'],
                ['骑行裤', 'shorts', 'bib', '裤子'],
                ['手套', 'glove', '手套'],
                ['骑行鞋', 'shoe', '鞋子', '锁鞋'],
                ['袜子', 'sock', '袜']
            ],
            '骑行配件': [
                ['车灯', 'light', '灯', '照明'],
                ['码表', 'computer', '码表', '速度'],
                ['水壶', 'bottle', '水壶', '水杯'],
                ['车锁', 'lock', '锁'],
                ['打气筒', 'pump', '打气', '充气'],
                ['工具', 'tool', '扳手', '六角']
            ],
            '自行车零件': [
                ['轮胎', 'tire', '外胎'],
                ['内胎', 'tube', '内胎'],
                ['刹车', 'brake', '制动'],
                ['链条', 'chain', '链条'],
                ['齿轮', 'gear', '飞轮', 'cassette'],
                ['座垫', 'saddle', '坐垫', '座包'],
                ['把手', 'handlebar', '车把'],
                ['轮组', 'wheel', '轮圈']
            ]
        }
        
        for category, rule_groups in classification_rules.items():
            for rules in rule_groups:
                if any(rule in text for rule in rules):
                    return category
        
        return '其他'
    
    def get_task_status(self, task_id: str) -> Dict:
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
    
    def get_all_tasks(self) -> List[Dict]:
        """获取所有任务状态"""
        tasks = []
        for task_id in self.tasks:
            try:
                task_status = self.get_task_status(task_id)
                tasks.append(task_status)
            except Exception as e:
                logger.error(f"获取任务状态失败: {task_id}: {str(e)}")
        return tasks
    
    def cleanup_old_tasks(self, days: int = 7):
        """清理旧任务记录"""
        cutoff_time = datetime.now() - timedelta(days=days)
        
        tasks_to_remove = []
        for task_id, task in self.tasks.items():
            if 'start_time' in task and task['start_time'] < cutoff_time:
                tasks_to_remove.append(task_id)
        
        for task_id in tasks_to_remove:
            del self.tasks[task_id]
        
        logger.info(f"清理了 {len(tasks_to_remove)} 个旧任务记录")
        return len(tasks_to_remove)