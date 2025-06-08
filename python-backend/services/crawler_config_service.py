# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from loguru import logger

class CrawlerConfigService:
    """爬虫配置管理服务"""
    
    def __init__(self, config_file: str = 'crawler_config.json'):
        self.config_file = config_file
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'config', config_file)
        self.default_config = self._get_default_config()
        self.config = self._load_config()
    
    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            'crawler_settings': {
                'request_delay': {
                    'min': 2,
                    'max': 5,
                    'description': '请求间隔时间范围（秒）'
                },
                'max_retries': {
                    'value': 3,
                    'description': '最大重试次数'
                },
                'timeout': {
                    'value': 30,
                    'description': '请求超时时间（秒）'
                },
                'max_workers': {
                    'value': 3,
                    'description': '最大并发线程数'
                },
                'max_items_per_keyword': {
                    'value': 50,
                    'description': '每个关键词最大爬取商品数'
                },
                'enable_proxy': {
                    'value': False,
                    'description': '是否启用代理'
                },
                'enable_headless': {
                    'value': True,
                    'description': '是否启用无头浏览器'
                }
            },
            'anti_detection': {
                'user_agent_rotation': {
                    'enabled': True,
                    'description': '是否启用User-Agent轮换'
                },
                'random_delays': {
                    'enabled': True,
                    'description': '是否启用随机延迟'
                },
                'disable_images': {
                    'enabled': True,
                    'description': '是否禁用图片加载'
                },
                'stealth_mode': {
                    'enabled': True,
                    'description': '是否启用隐身模式'
                }
            },
            'platforms': {
                'taobao': {
                    'enabled': True,
                    'name': '淘宝',
                    'search_url': 'https://s.taobao.com/search?q={keyword}&sort=sale-desc',
                    'selectors': {
                        'items': '.item',
                        'title': '.title a',
                        'price': '.price strong',
                        'image': '.pic img',
                        'shop': '.shop a',
                        'sales': '.deal-cnt'
                    },
                    'rate_limit': {
                        'requests_per_minute': 30,
                        'description': '每分钟最大请求数'
                    }
                },
                'jd': {
                    'enabled': True,
                    'name': '京东',
                    'search_url': 'https://search.jd.com/Search?keyword={keyword}&enc=utf-8',
                    'selectors': {
                        'items': '.gl-item',
                        'title': '.p-name a em',
                        'price': '.p-price i',
                        'image': '.p-img img',
                        'shop': '.p-shop a',
                        'sales': '.p-commit a'
                    },
                    'rate_limit': {
                        'requests_per_minute': 40,
                        'description': '每分钟最大请求数'
                    }
                },
                'tmall': {
                    'enabled': False,
                    'name': '天猫',
                    'search_url': 'https://list.tmall.com/search_product.htm?q={keyword}&sort=s&style=g',
                    'selectors': {
                        'items': '.product',
                        'title': '.productTitle a',
                        'price': '.productPrice em',
                        'image': '.productImg img',
                        'shop': '.productShop a',
                        'sales': '.productStatus span'
                    },
                    'rate_limit': {
                        'requests_per_minute': 20,
                        'description': '每分钟最大请求数'
                    }
                }
            },
            'categories': {
                'bike': {
                    'name': '自行车',
                    'enabled': True,
                    'keywords': ['自行车', '山地车', '公路车', '折叠车', '电动车', '单车', 'bike', 'bicycle'],
                    'subcategories': ['山地车', '公路车', '折叠车', '电动车', '城市车', '儿童车'],
                    'priority': 1
                },
                'helmet': {
                    'name': '头盔',
                    'enabled': True,
                    'keywords': ['头盔', '骑行头盔', '安全帽', 'helmet', '防护帽'],
                    'subcategories': ['山地头盔', '公路头盔', '城市头盔', '儿童头盔'],
                    'priority': 2
                },
                'clothing': {
                    'name': '骑行服装',
                    'enabled': True,
                    'keywords': ['骑行服', '骑行裤', '骑行手套', '骑行鞋', '骑行袜', 'jersey', 'shorts'],
                    'subcategories': ['骑行上衣', '骑行裤', '骑行手套', '骑行鞋', '骑行袜子'],
                    'priority': 3
                },
                'accessories': {
                    'name': '骑行配件',
                    'enabled': True,
                    'keywords': ['车灯', '码表', '水壶', '车锁', '打气筒', '工具包', 'light', 'computer'],
                    'subcategories': ['车灯', '码表', '水壶架', '车锁', '打气筒', '维修工具'],
                    'priority': 4
                },
                'parts': {
                    'name': '自行车零件',
                    'enabled': True,
                    'keywords': ['轮胎', '内胎', '刹车片', '链条', '齿轮', '座垫', 'tire', 'brake'],
                    'subcategories': ['轮胎', '内胎', '刹车系统', '传动系统', '座垫', '把手'],
                    'priority': 5
                },
                'safety': {
                    'name': '安全防护',
                    'enabled': True,
                    'keywords': ['护膝', '护肘', '护具', '反光衣', '尾灯', '铃铛'],
                    'subcategories': ['护具', '反光装备', '警示装备'],
                    'priority': 6
                }
            },
            'data_quality': {
                'min_title_length': {
                    'value': 5,
                    'description': '商品标题最小长度'
                },
                'max_title_length': {
                    'value': 200,
                    'description': '商品标题最大长度'
                },
                'min_price': {
                    'value': 1,
                    'description': '最小价格（元）'
                },
                'max_price': {
                    'value': 100000,
                    'description': '最大价格（元）'
                },
                'required_fields': {
                    'value': ['name', 'price', 'platform'],
                    'description': '必需字段列表'
                },
                'duplicate_check': {
                    'enabled': True,
                    'fields': ['name', 'platform_url'],
                    'description': '重复检查配置'
                }
            },
            'scheduling': {
                'daily_crawl': {
                    'enabled': True,
                    'time': '02:00',
                    'description': '每日全量爬取时间'
                },
                'price_update': {
                    'enabled': True,
                    'interval_hours': 4,
                    'description': '价格更新间隔（小时）'
                },
                'cleanup': {
                    'enabled': True,
                    'interval_hours': 1,
                    'keep_days': 7,
                    'description': '任务清理配置'
                }
            },
            'proxy_settings': {
                'enabled': False,
                'proxy_list': [],
                'rotation_strategy': 'round_robin',
                'test_url': 'https://httpbin.org/ip',
                'timeout': 10,
                'max_failures': 3
            },
            'notification': {
                'email': {
                    'enabled': False,
                    'smtp_server': '',
                    'smtp_port': 587,
                    'username': '',
                    'password': '',
                    'recipients': []
                },
                'webhook': {
                    'enabled': False,
                    'url': '',
                    'events': ['task_completed', 'task_failed', 'price_alert']
                }
            },
            'logging': {
                'level': 'INFO',
                'file_path': 'logs/crawler.log',
                'max_file_size': '10MB',
                'backup_count': 5,
                'format': '{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}'
            },
            'version': '1.0.0',
            'last_updated': datetime.now().isoformat()
        }
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        try:
            # 确保配置目录存在
            config_dir = os.path.dirname(self.config_path)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 合并默认配置和用户配置
                merged_config = self._merge_config(self.default_config, config)
                return merged_config
            else:
                # 如果配置文件不存在，创建默认配置文件
                self._save_config(self.default_config)
                return self.default_config.copy()
        
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            return self.default_config.copy()
    
    def _merge_config(self, default: Dict, user: Dict) -> Dict:
        """合并默认配置和用户配置"""
        merged = default.copy()
        
        for key, value in user.items():
            if key in merged:
                if isinstance(value, dict) and isinstance(merged[key], dict):
                    merged[key] = self._merge_config(merged[key], value)
                else:
                    merged[key] = value
            else:
                merged[key] = value
        
        return merged
    
    def _save_config(self, config: Dict = None) -> bool:
        """保存配置文件"""
        try:
            if config is None:
                config = self.config
            
            # 更新最后修改时间
            config['last_updated'] = datetime.now().isoformat()
            
            # 确保配置目录存在
            config_dir = os.path.dirname(self.config_path)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            logger.info(f"配置文件已保存: {self.config_path}")
            return True
        
        except Exception as e:
            logger.error(f"保存配置文件失败: {str(e)}")
            return False
    
    def get_config(self, key_path: str = None) -> Any:
        """获取配置值"""
        if key_path is None:
            return self.config
        
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            logger.warning(f"配置键不存在: {key_path}")
            return None
    
    def set_config(self, key_path: str, value: Any) -> bool:
        """设置配置值"""
        keys = key_path.split('.')
        config = self.config
        
        try:
            # 导航到父级配置
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            
            # 设置值
            config[keys[-1]] = value
            
            # 保存配置
            return self._save_config()
        
        except Exception as e:
            logger.error(f"设置配置失败: {key_path} = {value}: {str(e)}")
            return False
    
    def get_enabled_platforms(self) -> List[str]:
        """获取启用的平台列表"""
        platforms = []
        platform_configs = self.get_config('platforms') or {}
        
        for platform_id, config in platform_configs.items():
            if config.get('enabled', False):
                platforms.append(platform_id)
        
        return platforms
    
    def get_enabled_categories(self) -> List[str]:
        """获取启用的分类列表"""
        categories = []
        category_configs = self.get_config('categories') or {}
        
        for category_id, config in category_configs.items():
            if config.get('enabled', False):
                categories.append(category_id)
        
        # 按优先级排序
        categories.sort(key=lambda x: category_configs[x].get('priority', 999))
        return categories
    
    def get_keywords_by_category(self, category: str) -> List[str]:
        """获取分类的关键词列表"""
        category_config = self.get_config(f'categories.{category}')
        if category_config:
            return category_config.get('keywords', [])
        return []
    
    def get_platform_config(self, platform: str) -> Optional[Dict]:
        """获取平台配置"""
        return self.get_config(f'platforms.{platform}')
    
    def get_crawler_settings(self) -> Dict:
        """获取爬虫设置"""
        return self.get_config('crawler_settings') or {}
    
    def get_anti_detection_settings(self) -> Dict:
        """获取反检测设置"""
        return self.get_config('anti_detection') or {}
    
    def get_data_quality_settings(self) -> Dict:
        """获取数据质量设置"""
        return self.get_config('data_quality') or {}
    
    def get_proxy_settings(self) -> Dict:
        """获取代理设置"""
        return self.get_config('proxy_settings') or {}
    
    def update_platform_status(self, platform: str, enabled: bool) -> bool:
        """更新平台启用状态"""
        return self.set_config(f'platforms.{platform}.enabled', enabled)
    
    def update_category_status(self, category: str, enabled: bool) -> bool:
        """更新分类启用状态"""
        return self.set_config(f'categories.{category}.enabled', enabled)
    
    def add_keywords_to_category(self, category: str, keywords: List[str]) -> bool:
        """向分类添加关键词"""
        current_keywords = self.get_keywords_by_category(category)
        new_keywords = list(set(current_keywords + keywords))
        return self.set_config(f'categories.{category}.keywords', new_keywords)
    
    def remove_keywords_from_category(self, category: str, keywords: List[str]) -> bool:
        """从分类移除关键词"""
        current_keywords = self.get_keywords_by_category(category)
        new_keywords = [k for k in current_keywords if k not in keywords]
        return self.set_config(f'categories.{category}.keywords', new_keywords)
    
    def reset_to_default(self) -> bool:
        """重置为默认配置"""
        try:
            self.config = self.default_config.copy()
            return self._save_config()
        except Exception as e:
            logger.error(f"重置配置失败: {str(e)}")
            return False
    
    def export_config(self, file_path: str) -> bool:
        """导出配置到文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            logger.info(f"配置已导出到: {file_path}")
            return True
        except Exception as e:
            logger.error(f"导出配置失败: {str(e)}")
            return False
    
    def import_config(self, file_path: str) -> bool:
        """从文件导入配置"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # 验证配置格式
            if self._validate_config(imported_config):
                self.config = self._merge_config(self.default_config, imported_config)
                return self._save_config()
            else:
                logger.error("导入的配置格式无效")
                return False
        
        except Exception as e:
            logger.error(f"导入配置失败: {str(e)}")
            return False
    
    def _validate_config(self, config: Dict) -> bool:
        """验证配置格式"""
        required_sections = ['crawler_settings', 'platforms', 'categories']
        
        for section in required_sections:
            if section not in config:
                logger.error(f"配置缺少必需部分: {section}")
                return False
        
        return True
    
    def get_config_summary(self) -> Dict:
        """获取配置摘要"""
        enabled_platforms = self.get_enabled_platforms()
        enabled_categories = self.get_enabled_categories()
        
        total_keywords = 0
        for category in enabled_categories:
            keywords = self.get_keywords_by_category(category)
            total_keywords += len(keywords)
        
        return {
            'version': self.get_config('version'),
            'last_updated': self.get_config('last_updated'),
            'enabled_platforms': enabled_platforms,
            'enabled_categories': enabled_categories,
            'total_keywords': total_keywords,
            'crawler_settings': {
                'max_workers': self.get_config('crawler_settings.max_workers.value'),
                'max_retries': self.get_config('crawler_settings.max_retries.value'),
                'timeout': self.get_config('crawler_settings.timeout.value'),
                'enable_proxy': self.get_config('crawler_settings.enable_proxy.value')
            },
            'anti_detection': {
                'user_agent_rotation': self.get_config('anti_detection.user_agent_rotation.enabled'),
                'random_delays': self.get_config('anti_detection.random_delays.enabled'),
                'stealth_mode': self.get_config('anti_detection.stealth_mode.enabled')
            }
        }