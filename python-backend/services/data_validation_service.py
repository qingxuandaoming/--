import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from loguru import logger
from urllib.parse import urlparse
import hashlib

class DataValidationService:
    """数据验证和清洗服务类"""
    
    def __init__(self):
        # 价格范围配置
        self.price_ranges = {
            '自行车': {'min': 100, 'max': 50000},
            '安全防护': {'min': 20, 'max': 2000},
            '骑行服装': {'min': 10, 'max': 3000},
            '骑行配件': {'min': 5, 'max': 5000},
            '自行车零件': {'min': 10, 'max': 10000},
            '其他': {'min': 1, 'max': 100000}
        }
        
        # 标题长度限制
        self.title_length = {'min': 5, 'max': 200}
        
        # 必需字段
        self.required_fields = ['name', 'platform', 'price']
        
        # 平台域名映射
        self.platform_domains = {
            'taobao': ['taobao.com', 'tmall.com'],
            'jd': ['jd.com', '360buy.com'],
            'tmall': ['tmall.com']
        }
        
        # 数据去重缓存
        self.duplicate_cache = set()
        
    def validate_equipment_data(self, data: Dict) -> Dict:
        """验证装备数据"""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'cleaned_data': data.copy()
        }
        
        try:
            # 1. 检查必需字段
            self._check_required_fields(data, validation_result)
            
            # 2. 清洗和验证商品名称
            self._validate_and_clean_name(data, validation_result)
            
            # 3. 验证和清洗价格
            self._validate_and_clean_price(data, validation_result)
            
            # 4. 验证平台信息
            self._validate_platform(data, validation_result)
            
            # 5. 清洗URL
            self._clean_urls(data, validation_result)
            
            # 6. 验证图片URL
            self._validate_image_url(data, validation_result)
            
            # 7. 清洗店铺信息
            self._clean_shop_info(data, validation_result)
            
            # 8. 验证销量数据
            self._validate_sales_data(data, validation_result)
            
            # 9. 检查重复数据
            self._check_duplicate(data, validation_result)
            
            # 10. 添加数据质量评分
            self._calculate_quality_score(validation_result)
            
        except Exception as e:
            logger.error(f"数据验证过程中出错: {str(e)}")
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"验证过程异常: {str(e)}")
        
        return validation_result
    
    def _check_required_fields(self, data: Dict, result: Dict):
        """检查必需字段"""
        for field in self.required_fields:
            if field not in data or not data[field]:
                result['is_valid'] = False
                result['errors'].append(f"缺少必需字段: {field}")
    
    def _validate_and_clean_name(self, data: Dict, result: Dict):
        """验证和清洗商品名称"""
        if 'name' not in data:
            return
        
        name = str(data['name']).strip()
        
        # 移除HTML标签
        name = re.sub(r'<[^>]+>', '', name)
        
        # 移除多余的空格
        name = re.sub(r'\s+', ' ', name)
        
        # 移除特殊字符（保留中文、英文、数字、常用符号）
        name = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s\-_()（）【】\[\]/.,，。]', '', name)
        
        # 检查长度
        if len(name) < self.title_length['min']:
            result['errors'].append(f"商品名称过短: {len(name)}字符")
            result['is_valid'] = False
        elif len(name) > self.title_length['max']:
            name = name[:self.title_length['max']]
            result['warnings'].append(f"商品名称过长，已截断至{self.title_length['max']}字符")
        
        # 检查是否为有效的商品名称
        if not self._is_valid_product_name(name):
            result['warnings'].append("商品名称可能不是有效的产品名称")
        
        result['cleaned_data']['name'] = name
    
    def _validate_and_clean_price(self, data: Dict, result: Dict):
        """验证和清洗价格"""
        if 'price' not in data:
            return
        
        price = data['price']
        
        # 转换价格为浮点数
        if isinstance(price, str):
            # 移除货币符号和逗号
            price_str = re.sub(r'[¥$,，]', '', price)
            # 提取数字
            price_match = re.search(r'\d+\.?\d*', price_str)
            if price_match:
                price = float(price_match.group())
            else:
                result['errors'].append(f"无法解析价格: {data['price']}")
                result['is_valid'] = False
                return
        
        try:
            price = float(price)
        except (ValueError, TypeError):
            result['errors'].append(f"价格格式错误: {data['price']}")
            result['is_valid'] = False
            return
        
        # 检查价格范围
        category = data.get('category', '其他')
        price_range = self.price_ranges.get(category, self.price_ranges['其他'])
        
        if price < price_range['min']:
            result['warnings'].append(f"价格过低: ¥{price}，分类: {category}")
        elif price > price_range['max']:
            result['warnings'].append(f"价格过高: ¥{price}，分类: {category}")
        
        # 价格为0的情况
        if price <= 0:
            result['errors'].append("价格不能为0或负数")
            result['is_valid'] = False
        
        result['cleaned_data']['price'] = round(price, 2)
    
    def _validate_platform(self, data: Dict, result: Dict):
        """验证平台信息"""
        if 'platform' not in data:
            return
        
        platform = data['platform'].lower().strip()
        
        # 标准化平台名称
        platform_mapping = {
            'taobao': 'taobao',
            '淘宝': 'taobao',
            'jd': 'jd',
            '京东': 'jd',
            'tmall': 'tmall',
            '天猫': 'tmall'
        }
        
        if platform in platform_mapping:
            result['cleaned_data']['platform'] = platform_mapping[platform]
        else:
            result['warnings'].append(f"未知平台: {platform}")
            result['cleaned_data']['platform'] = platform
    
    def _clean_urls(self, data: Dict, result: Dict):
        """清洗URL"""
        url_fields = ['platform_url', 'shop_url']
        
        for field in url_fields:
            if field in data and data[field]:
                url = str(data[field]).strip()
                
                # 补全协议
                if url.startswith('//'):
                    url = 'https:' + url
                elif not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                # 验证URL格式
                try:
                    parsed = urlparse(url)
                    if not parsed.netloc:
                        result['warnings'].append(f"URL格式可能有误: {field}")
                except Exception:
                    result['warnings'].append(f"URL解析失败: {field}")
                
                result['cleaned_data'][field] = url
    
    def _validate_image_url(self, data: Dict, result: Dict):
        """验证图片URL"""
        if 'image_url' not in data or not data['image_url']:
            result['warnings'].append("缺少商品图片")
            return
        
        image_url = str(data['image_url']).strip()
        
        # 补全协议
        if image_url.startswith('//'):
            image_url = 'https:' + image_url
        elif not image_url.startswith(('http://', 'https://')):
            image_url = 'https://' + image_url
        
        # 检查是否为图片URL
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
        if not any(image_url.lower().endswith(ext) for ext in image_extensions):
            # 检查URL中是否包含图片相关参数
            if not any(param in image_url.lower() for param in ['img', 'image', 'pic', 'photo']):
                result['warnings'].append("图片URL可能不是有效的图片链接")
        
        result['cleaned_data']['image_url'] = image_url
    
    def _clean_shop_info(self, data: Dict, result: Dict):
        """清洗店铺信息"""
        if 'shop_name' in data and data['shop_name']:
            shop_name = str(data['shop_name']).strip()
            
            # 移除多余的空格和特殊字符
            shop_name = re.sub(r'\s+', ' ', shop_name)
            shop_name = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s\-_()（）]', '', shop_name)
            
            # 限制长度
            if len(shop_name) > 100:
                shop_name = shop_name[:100]
                result['warnings'].append("店铺名称过长，已截断")
            
            result['cleaned_data']['shop_name'] = shop_name
    
    def _validate_sales_data(self, data: Dict, result: Dict):
        """验证销量数据"""
        sales_fields = ['sales', 'commit_count', 'rating_count']
        
        for field in sales_fields:
            if field in data and data[field] is not None:
                try:
                    sales = int(data[field])
                    if sales < 0:
                        result['warnings'].append(f"{field}不能为负数")
                        sales = 0
                    result['cleaned_data'][field] = sales
                except (ValueError, TypeError):
                    result['warnings'].append(f"{field}格式错误: {data[field]}")
                    result['cleaned_data'][field] = 0
    
    def _check_duplicate(self, data: Dict, result: Dict):
        """检查重复数据"""
        # 生成数据指纹
        fingerprint_data = {
            'name': data.get('name', ''),
            'platform': data.get('platform', ''),
            'price': data.get('price', 0)
        }
        
        fingerprint = hashlib.md5(
            json.dumps(fingerprint_data, sort_keys=True).encode()
        ).hexdigest()
        
        if fingerprint in self.duplicate_cache:
            result['warnings'].append("检测到可能的重复数据")
            result['is_duplicate'] = True
        else:
            self.duplicate_cache.add(fingerprint)
            result['is_duplicate'] = False
    
    def _calculate_quality_score(self, result: Dict):
        """计算数据质量评分"""
        score = 100
        
        # 错误扣分
        score -= len(result['errors']) * 20
        
        # 警告扣分
        score -= len(result['warnings']) * 5
        
        # 重复数据扣分
        if result.get('is_duplicate', False):
            score -= 10
        
        # 检查数据完整性
        data = result['cleaned_data']
        completeness_fields = ['name', 'price', 'image_url', 'shop_name', 'platform_url']
        missing_fields = sum(1 for field in completeness_fields if not data.get(field))
        score -= missing_fields * 3
        
        result['quality_score'] = max(0, min(100, score))
    
    def _is_valid_product_name(self, name: str) -> bool:
        """检查是否为有效的商品名称"""
        # 检查是否包含骑行相关关键词
        cycling_keywords = [
            '自行车', '山地车', '公路车', '折叠车', '电动车',
            '头盔', '骑行', '单车', '脚踏车',
            'bike', 'bicycle', 'cycling', 'helmet'
        ]
        
        name_lower = name.lower()
        return any(keyword in name_lower for keyword in cycling_keywords)
    
    def batch_validate(self, data_list: List[Dict]) -> List[Dict]:
        """批量验证数据"""
        results = []
        
        for i, data in enumerate(data_list):
            try:
                result = self.validate_equipment_data(data)
                result['index'] = i
                results.append(result)
            except Exception as e:
                logger.error(f"批量验证第{i}条数据失败: {str(e)}")
                results.append({
                    'index': i,
                    'is_valid': False,
                    'errors': [f"验证异常: {str(e)}"],
                    'warnings': [],
                    'cleaned_data': data,
                    'quality_score': 0
                })
        
        return results
    
    def get_validation_summary(self, results: List[Dict]) -> Dict:
        """获取验证结果摘要"""
        total = len(results)
        valid = sum(1 for r in results if r['is_valid'])
        invalid = total - valid
        
        total_errors = sum(len(r['errors']) for r in results)
        total_warnings = sum(len(r['warnings']) for r in results)
        
        avg_quality_score = sum(r.get('quality_score', 0) for r in results) / total if total > 0 else 0
        
        return {
            'total_records': total,
            'valid_records': valid,
            'invalid_records': invalid,
            'validation_rate': round(valid / total * 100, 2) if total > 0 else 0,
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'average_quality_score': round(avg_quality_score, 2),
            'quality_distribution': self._get_quality_distribution(results)
        }
    
    def _get_quality_distribution(self, results: List[Dict]) -> Dict:
        """获取质量分布"""
        distribution = {
            'excellent': 0,  # 90-100
            'good': 0,       # 70-89
            'fair': 0,       # 50-69
            'poor': 0        # 0-49
        }
        
        for result in results:
            score = result.get('quality_score', 0)
            if score >= 90:
                distribution['excellent'] += 1
            elif score >= 70:
                distribution['good'] += 1
            elif score >= 50:
                distribution['fair'] += 1
            else:
                distribution['poor'] += 1
        
        return distribution
    
    def clear_duplicate_cache(self):
        """清空重复数据缓存"""
        self.duplicate_cache.clear()
        logger.info("重复数据缓存已清空")