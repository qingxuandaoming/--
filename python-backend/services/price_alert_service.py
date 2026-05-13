import json
import smtplib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from loguru import logger
import requests
import threading
import time

class PriceAlertService:
    """价格预警服务类"""
    
    def __init__(self):
        self.alerts = {}  # 存储价格预警规则
        self.alert_history = []  # 预警历史记录
        self.is_monitoring = False
        self.monitor_thread = None
        
        # 邮件配置
        self.email_config = {
            'smtp_server': 'smtp.qq.com',
            'smtp_port': 587,
            'username': '',
            'password': '',
            'from_email': ''
        }
        
        # Webhook配置
        self.webhook_config = {
            'enabled': False,
            'url': '',
            'headers': {}
        }
        
        # 预警类型
        self.alert_types = {
            'price_drop': '价格下降',
            'price_rise': '价格上涨',
            'target_price': '目标价格',
            'percentage_change': '百分比变化'
        }
    
    def create_price_alert(self, equipment_id: int, alert_type: str, 
                          threshold: float, user_email: str = None, 
                          user_id: int = None, enabled: bool = True) -> str:
        """创建价格预警"""
        try:
            from app import db, Equipment
            
            # 验证装备是否存在
            equipment = Equipment.query.get(equipment_id)
            if not equipment:
                raise ValueError(f"装备 {equipment_id} 不存在")
            
            # 验证预警类型
            if alert_type not in self.alert_types:
                raise ValueError(f"无效的预警类型: {alert_type}")
            
            # 生成预警ID
            alert_id = f"alert_{equipment_id}_{int(datetime.now().timestamp())}"
            
            # 创建预警规则
            alert_rule = {
                'id': alert_id,
                'equipment_id': equipment_id,
                'equipment_name': equipment.name,
                'alert_type': alert_type,
                'threshold': threshold,
                'user_email': user_email,
                'user_id': user_id,
                'enabled': enabled,
                'created_at': datetime.now(),
                'last_checked': None,
                'last_triggered': None,
                'trigger_count': 0,
                'current_price': float(equipment.price)
            }
            
            self.alerts[alert_id] = alert_rule
            
            logger.info(f"创建价格预警: {alert_id} - {equipment.name} - {alert_type}")
            
            return alert_id
            
        except Exception as e:
            logger.error(f"创建价格预警失败: {str(e)}")
            raise
    
    def update_alert(self, alert_id: str, **kwargs) -> bool:
        """更新预警规则"""
        try:
            if alert_id not in self.alerts:
                raise ValueError(f"预警 {alert_id} 不存在")
            
            alert = self.alerts[alert_id]
            
            # 更新允许的字段
            updatable_fields = ['threshold', 'enabled', 'user_email']
            for field, value in kwargs.items():
                if field in updatable_fields:
                    alert[field] = value
            
            alert['updated_at'] = datetime.now()
            
            logger.info(f"更新价格预警: {alert_id}")
            return True
            
        except Exception as e:
            logger.error(f"更新价格预警失败: {str(e)}")
            return False
    
    def delete_alert(self, alert_id: str) -> bool:
        """删除预警规则"""
        try:
            if alert_id not in self.alerts:
                raise ValueError(f"预警 {alert_id} 不存在")
            
            del self.alerts[alert_id]
            
            logger.info(f"删除价格预警: {alert_id}")
            return True
            
        except Exception as e:
            logger.error(f"删除价格预警失败: {str(e)}")
            return False
    
    def get_alert(self, alert_id: str) -> Optional[Dict]:
        """获取预警规则"""
        alert = self.alerts.get(alert_id)
        if alert:
            # 转换datetime为字符串
            alert_copy = alert.copy()
            for key, value in alert_copy.items():
                if isinstance(value, datetime):
                    alert_copy[key] = value.isoformat()
            return alert_copy
        return None
    
    def get_user_alerts(self, user_id: int = None, user_email: str = None) -> List[Dict]:
        """获取用户的预警规则"""
        user_alerts = []
        
        for alert in self.alerts.values():
            if (user_id and alert.get('user_id') == user_id) or \
               (user_email and alert.get('user_email') == user_email):
                alert_copy = alert.copy()
                # 转换datetime为字符串
                for key, value in alert_copy.items():
                    if isinstance(value, datetime):
                        alert_copy[key] = value.isoformat()
                user_alerts.append(alert_copy)
        
        return user_alerts
    
    def start_monitoring(self, check_interval: int = 300):
        """启动价格监控"""
        if self.is_monitoring:
            logger.warning("价格监控已在运行")
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_prices,
            args=(check_interval,),
            daemon=True
        )
        self.monitor_thread.start()
        
        logger.info(f"价格监控已启动，检查间隔: {check_interval}秒")
    
    def stop_monitoring(self):
        """停止价格监控"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        logger.info("价格监控已停止")
    
    def _monitor_prices(self, check_interval: int):
        """监控价格变化"""
        while self.is_monitoring:
            try:
                self._check_all_alerts()
                time.sleep(check_interval)
            except Exception as e:
                logger.error(f"价格监控异常: {str(e)}")
                time.sleep(60)  # 出错后等待1分钟再继续
    
    def _check_all_alerts(self):
        """检查所有预警规则"""
        from app import db, Equipment, EquipmentPrice
        
        active_alerts = [alert for alert in self.alerts.values() if alert['enabled']]
        
        if not active_alerts:
            return
        
        logger.info(f"检查 {len(active_alerts)} 个活跃预警规则")
        
        for alert in active_alerts:
            try:
                # 获取最新价格
                latest_price = db.session.query(EquipmentPrice.price).filter(
                    EquipmentPrice.equipment_id == alert['equipment_id'],
                    EquipmentPrice.is_available == True
                ).order_by(EquipmentPrice.recorded_at.desc()).first()
                
                if not latest_price:
                    continue
                
                current_price = float(latest_price.price)
                previous_price = alert['current_price']
                
                # 更新当前价格和检查时间
                alert['current_price'] = current_price
                alert['last_checked'] = datetime.now()
                
                # 检查是否触发预警
                if self._should_trigger_alert(alert, current_price, previous_price):
                    self._trigger_alert(alert, current_price, previous_price)
                
            except Exception as e:
                logger.error(f"检查预警 {alert['id']} 失败: {str(e)}")
    
    def _should_trigger_alert(self, alert: Dict, current_price: float, previous_price: float) -> bool:
        """判断是否应该触发预警"""
        alert_type = alert['alert_type']
        threshold = alert['threshold']
        
        if alert_type == 'price_drop':
            # 价格下降超过阈值
            return current_price <= previous_price - threshold
        
        elif alert_type == 'price_rise':
            # 价格上涨超过阈值
            return current_price >= previous_price + threshold
        
        elif alert_type == 'target_price':
            # 达到目标价格
            return current_price <= threshold
        
        elif alert_type == 'percentage_change':
            # 百分比变化超过阈值
            if previous_price > 0:
                change_percent = abs(current_price - previous_price) / previous_price * 100
                return change_percent >= threshold
        
        return False
    
    def _trigger_alert(self, alert: Dict, current_price: float, previous_price: float):
        """触发预警"""
        try:
            # 更新触发信息
            alert['last_triggered'] = datetime.now()
            alert['trigger_count'] += 1
            
            # 创建预警记录
            alert_record = {
                'alert_id': alert['id'],
                'equipment_id': alert['equipment_id'],
                'equipment_name': alert['equipment_name'],
                'alert_type': alert['alert_type'],
                'threshold': alert['threshold'],
                'previous_price': previous_price,
                'current_price': current_price,
                'price_change': current_price - previous_price,
                'price_change_percent': ((current_price - previous_price) / previous_price * 100) if previous_price > 0 else 0,
                'triggered_at': datetime.now(),
                'user_email': alert.get('user_email'),
                'user_id': alert.get('user_id')
            }
            
            self.alert_history.append(alert_record)
            
            # 发送通知
            self._send_alert_notification(alert_record)
            
            logger.info(f"触发价格预警: {alert['id']} - {alert['equipment_name']} - ¥{current_price}")
            
        except Exception as e:
            logger.error(f"触发预警失败: {str(e)}")
    
    def _send_alert_notification(self, alert_record: Dict):
        """发送预警通知"""
        # 发送邮件通知
        if alert_record.get('user_email') and self.email_config.get('username'):
            self._send_email_notification(alert_record)
        
        # 发送Webhook通知
        if self.webhook_config.get('enabled') and self.webhook_config.get('url'):
            self._send_webhook_notification(alert_record)
    
    def _send_email_notification(self, alert_record: Dict):
        """发送邮件通知"""
        try:
            # 构建邮件内容
            subject = f"价格预警: {alert_record['equipment_name']}"
            
            body = f"""
            您好！
            
            您设置的价格预警已触发：
            
            商品名称: {alert_record['equipment_name']}
            预警类型: {self.alert_types.get(alert_record['alert_type'], alert_record['alert_type'])}
            阈值: ¥{alert_record['threshold']}
            原价格: ¥{alert_record['previous_price']:.2f}
            现价格: ¥{alert_record['current_price']:.2f}
            价格变化: ¥{alert_record['price_change']:.2f} ({alert_record['price_change_percent']:.1f}%)
            触发时间: {alert_record['triggered_at'].strftime('%Y-%m-%d %H:%M:%S')}
            
            请及时查看商品详情。
            
            此邮件由系统自动发送，请勿回复。
            """
            
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from_email']
            msg['To'] = alert_record['user_email']
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 发送邮件
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            
            text = msg.as_string()
            server.sendmail(self.email_config['from_email'], alert_record['user_email'], text)
            server.quit()
            
            logger.info(f"邮件通知已发送: {alert_record['user_email']}")
            
        except Exception as e:
            logger.error(f"发送邮件通知失败: {str(e)}")
    
    def _send_webhook_notification(self, alert_record: Dict):
        """发送Webhook通知"""
        try:
            # 准备数据
            payload = {
                'type': 'price_alert',
                'alert_id': alert_record['alert_id'],
                'equipment': {
                    'id': alert_record['equipment_id'],
                    'name': alert_record['equipment_name']
                },
                'alert': {
                    'type': alert_record['alert_type'],
                    'threshold': alert_record['threshold']
                },
                'price': {
                    'previous': alert_record['previous_price'],
                    'current': alert_record['current_price'],
                    'change': alert_record['price_change'],
                    'change_percent': alert_record['price_change_percent']
                },
                'triggered_at': alert_record['triggered_at'].isoformat(),
                'user_id': alert_record.get('user_id')
            }
            
            # 发送请求
            headers = {'Content-Type': 'application/json'}
            headers.update(self.webhook_config.get('headers', {}))
            
            response = requests.post(
                self.webhook_config['url'],
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"Webhook通知已发送: {self.webhook_config['url']}")
            else:
                logger.warning(f"Webhook通知失败: {response.status_code}")
            
        except Exception as e:
            logger.error(f"发送Webhook通知失败: {str(e)}")
    
    def configure_email(self, smtp_server: str, smtp_port: int, username: str, 
                       password: str, from_email: str):
        """配置邮件设置"""
        self.email_config.update({
            'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'username': username,
            'password': password,
            'from_email': from_email
        })
        
        logger.info("邮件配置已更新")
    
    def configure_webhook(self, url: str, headers: Dict = None, enabled: bool = True):
        """配置Webhook设置"""
        self.webhook_config.update({
            'url': url,
            'headers': headers or {},
            'enabled': enabled
        })
        
        logger.info("Webhook配置已更新")
    
    def get_alert_history(self, limit: int = 100, user_id: int = None, 
                         equipment_id: int = None) -> List[Dict]:
        """获取预警历史"""
        history = self.alert_history.copy()
        
        # 过滤条件
        if user_id:
            history = [h for h in history if h.get('user_id') == user_id]
        
        if equipment_id:
            history = [h for h in history if h['equipment_id'] == equipment_id]
        
        # 按时间倒序排列
        history.sort(key=lambda x: x['triggered_at'], reverse=True)
        
        # 限制数量
        history = history[:limit]
        
        # 转换datetime为字符串
        for record in history:
            if isinstance(record['triggered_at'], datetime):
                record['triggered_at'] = record['triggered_at'].isoformat()
        
        return history
    
    def get_alert_statistics(self) -> Dict:
        """获取预警统计信息"""
        total_alerts = len(self.alerts)
        active_alerts = len([a for a in self.alerts.values() if a['enabled']])
        total_triggers = sum(a['trigger_count'] for a in self.alerts.values())
        
        # 按类型统计
        type_stats = {}
        for alert in self.alerts.values():
            alert_type = alert['alert_type']
            if alert_type not in type_stats:
                type_stats[alert_type] = {'count': 0, 'triggers': 0}
            type_stats[alert_type]['count'] += 1
            type_stats[alert_type]['triggers'] += alert['trigger_count']
        
        return {
            'total_alerts': total_alerts,
            'active_alerts': active_alerts,
            'inactive_alerts': total_alerts - active_alerts,
            'total_triggers': total_triggers,
            'monitoring_status': self.is_monitoring,
            'alert_types': type_stats,
            'recent_triggers': len([h for h in self.alert_history 
                                  if (datetime.now() - h['triggered_at']).days <= 7])
        }
    
    def cleanup_old_history(self, days: int = 30):
        """清理旧的预警历史"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        old_count = len(self.alert_history)
        self.alert_history = [h for h in self.alert_history 
                             if h['triggered_at'] > cutoff_date]
        
        cleaned_count = old_count - len(self.alert_history)
        
        logger.info(f"清理了 {cleaned_count} 条旧预警记录")
        
        return cleaned_count