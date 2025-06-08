import time
import threading
from datetime import datetime, timedelta
from collections import defaultdict, deque
from typing import Dict, List, Optional, Any
import json
import os
from dataclasses import dataclass, asdict
from sqlalchemy import create_engine, text
from database import get_db_session
from models.equipment import Equipment
from models.price_history import PriceHistory
import logging

logger = logging.getLogger(__name__)

@dataclass
class CrawlerStats:
    """爬虫统计信息"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    items_crawled: int = 0
    items_saved: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: float = 0.0
    avg_response_time: float = 0.0
    error_rate: float = 0.0
    success_rate: float = 0.0
    platform: str = ""
    category: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        # 转换datetime为字符串
        if self.start_time:
            data['start_time'] = self.start_time.isoformat()
        if self.end_time:
            data['end_time'] = self.end_time.isoformat()
        return data

@dataclass
class SystemMetrics:
    """系统性能指标"""
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    network_io: Dict[str, float] = None
    active_threads: int = 0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.network_io is None:
            self.network_io = {'bytes_sent': 0.0, 'bytes_recv': 0.0}
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data

class CrawlerMonitorService:
    """爬虫监控服务"""
    
    def __init__(self):
        self.stats_file = 'crawler_stats.json'
        self.metrics_file = 'system_metrics.json'
        self.max_history_size = 1000  # 最大历史记录数
        
        # 实时统计
        self.current_stats: Dict[str, CrawlerStats] = {}
        self.stats_history: deque = deque(maxlen=self.max_history_size)
        
        # 系统指标
        self.current_metrics: SystemMetrics = SystemMetrics()
        self.metrics_history: deque = deque(maxlen=self.max_history_size)
        
        # 错误统计
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.error_history: deque = deque(maxlen=100)
        
        # 性能指标
        self.response_times: deque = deque(maxlen=1000)
        self.request_rates: deque = deque(maxlen=100)
        
        # 监控状态
        self.monitoring_active = False
        self.monitor_thread = None
        self.lock = threading.Lock()
        
        # 加载历史数据
        self._load_stats_history()
        
    def start_monitoring(self):
        """开始监控"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            logger.info("爬虫监控服务已启动")
    
    def stop_monitoring(self):
        """停止监控"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self._save_stats_history()
        logger.info("爬虫监控服务已停止")
    
    def _monitor_loop(self):
        """监控循环"""
        while self.monitoring_active:
            try:
                # 收集系统指标
                self._collect_system_metrics()
                
                # 计算性能指标
                self._calculate_performance_metrics()
                
                # 保存历史数据
                if len(self.metrics_history) % 60 == 0:  # 每分钟保存一次
                    self._save_stats_history()
                
                time.sleep(1)  # 每秒收集一次
                
            except Exception as e:
                logger.error(f"监控循环错误: {str(e)}")
                time.sleep(5)
    
    def _collect_system_metrics(self):
        """收集系统性能指标"""
        try:
            import psutil
            
            metrics = SystemMetrics(
                cpu_usage=psutil.cpu_percent(),
                memory_usage=psutil.virtual_memory().percent,
                disk_usage=psutil.disk_usage('/').percent,
                network_io={
                    'bytes_sent': psutil.net_io_counters().bytes_sent,
                    'bytes_recv': psutil.net_io_counters().bytes_recv
                },
                active_threads=threading.active_count()
            )
            
            with self.lock:
                self.current_metrics = metrics
                self.metrics_history.append(metrics)
                
        except ImportError:
            logger.warning("psutil未安装，无法收集系统指标")
        except Exception as e:
            logger.error(f"收集系统指标失败: {str(e)}")
    
    def _calculate_performance_metrics(self):
        """计算性能指标"""
        with self.lock:
            # 计算平均响应时间
            if self.response_times:
                avg_response_time = sum(self.response_times) / len(self.response_times)
                for stats in self.current_stats.values():
                    stats.avg_response_time = avg_response_time
            
            # 计算请求速率
            current_time = time.time()
            self.request_rates.append((current_time, sum(stats.total_requests for stats in self.current_stats.values())))
    
    def start_crawl_session(self, session_id: str, platform: str, category: str = ""):
        """开始爬虫会话"""
        with self.lock:
            stats = CrawlerStats(
                platform=platform,
                category=category,
                start_time=datetime.now()
            )
            self.current_stats[session_id] = stats
            logger.info(f"开始爬虫会话: {session_id} - {platform}")
    
    def end_crawl_session(self, session_id: str):
        """结束爬虫会话"""
        with self.lock:
            if session_id in self.current_stats:
                stats = self.current_stats[session_id]
                stats.end_time = datetime.now()
                if stats.start_time:
                    stats.duration = (stats.end_time - stats.start_time).total_seconds()
                
                # 计算成功率和错误率
                if stats.total_requests > 0:
                    stats.success_rate = (stats.successful_requests / stats.total_requests) * 100
                    stats.error_rate = (stats.failed_requests / stats.total_requests) * 100
                
                # 添加到历史记录
                self.stats_history.append(stats)
                
                # 移除当前会话
                del self.current_stats[session_id]
                
                logger.info(f"结束爬虫会话: {session_id} - 耗时: {stats.duration:.2f}秒")
    
    def record_request(self, session_id: str, success: bool, response_time: float = 0.0):
        """记录请求"""
        with self.lock:
            if session_id in self.current_stats:
                stats = self.current_stats[session_id]
                stats.total_requests += 1
                
                if success:
                    stats.successful_requests += 1
                else:
                    stats.failed_requests += 1
                
                if response_time > 0:
                    self.response_times.append(response_time)
    
    def record_item_crawled(self, session_id: str, saved: bool = False):
        """记录爬取的商品"""
        with self.lock:
            if session_id in self.current_stats:
                stats = self.current_stats[session_id]
                stats.items_crawled += 1
                
                if saved:
                    stats.items_saved += 1
    
    def record_error(self, session_id: str, error_type: str, error_message: str):
        """记录错误"""
        with self.lock:
            self.error_counts[error_type] += 1
            
            error_record = {
                'session_id': session_id,
                'error_type': error_type,
                'error_message': error_message,
                'timestamp': datetime.now().isoformat()
            }
            self.error_history.append(error_record)
    
    def get_current_stats(self) -> Dict[str, Dict[str, Any]]:
        """获取当前统计信息"""
        with self.lock:
            return {session_id: stats.to_dict() for session_id, stats in self.current_stats.items()}
    
    def get_stats_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取统计历史"""
        with self.lock:
            history = list(self.stats_history)[-limit:]
            return [stats.to_dict() for stats in history]
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """获取系统指标"""
        with self.lock:
            return self.current_metrics.to_dict()
    
    def get_metrics_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取系统指标历史"""
        with self.lock:
            history = list(self.metrics_history)[-limit:]
            return [metrics.to_dict() for metrics in history]
    
    def get_error_summary(self) -> Dict[str, Any]:
        """获取错误摘要"""
        with self.lock:
            total_errors = sum(self.error_counts.values())
            recent_errors = list(self.error_history)[-10:]
            
            return {
                'total_errors': total_errors,
                'error_types': dict(self.error_counts),
                'recent_errors': recent_errors
            }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """获取性能摘要"""
        with self.lock:
            # 计算平均响应时间
            avg_response_time = 0.0
            if self.response_times:
                avg_response_time = sum(self.response_times) / len(self.response_times)
            
            # 计算请求速率
            request_rate = 0.0
            if len(self.request_rates) >= 2:
                recent_rates = list(self.request_rates)[-10:]
                if len(recent_rates) >= 2:
                    time_diff = recent_rates[-1][0] - recent_rates[0][0]
                    request_diff = recent_rates[-1][1] - recent_rates[0][1]
                    if time_diff > 0:
                        request_rate = request_diff / time_diff
            
            return {
                'avg_response_time': avg_response_time,
                'request_rate': request_rate,
                'active_sessions': len(self.current_stats),
                'total_requests': sum(stats.total_requests for stats in self.current_stats.values()),
                'total_items_crawled': sum(stats.items_crawled for stats in self.current_stats.values())
            }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """获取数据库统计信息"""
        try:
            with get_db_session() as session:
                # 设备总数
                total_equipment = session.query(Equipment).count()
                
                # 今日新增设备
                today = datetime.now().date()
                today_equipment = session.query(Equipment).filter(
                    Equipment.created_at >= today
                ).count()
                
                # 价格历史记录总数
                total_price_history = session.query(PriceHistory).count()
                
                # 今日价格更新
                today_price_updates = session.query(PriceHistory).filter(
                    PriceHistory.recorded_at >= today
                ).count()
                
                # 平台分布
                platform_stats = session.execute(
                    text("""
                    SELECT platform_url, COUNT(*) as count 
                    FROM equipment 
                    GROUP BY platform_url
                    """)
                ).fetchall()
                
                # 分类分布
                category_stats = session.execute(
                    text("""
                    SELECT category, COUNT(*) as count 
                    FROM equipment 
                    WHERE category IS NOT NULL
                    GROUP BY category
                    """)
                ).fetchall()
                
                return {
                    'total_equipment': total_equipment,
                    'today_equipment': today_equipment,
                    'total_price_history': total_price_history,
                    'today_price_updates': today_price_updates,
                    'platform_distribution': [{'platform': row[0], 'count': row[1]} for row in platform_stats],
                    'category_distribution': [{'category': row[0], 'count': row[1]} for row in category_stats]
                }
                
        except Exception as e:
            logger.error(f"获取数据库统计失败: {str(e)}")
            return {
                'error': f'获取数据库统计失败: {str(e)}'
            }
    
    def get_comprehensive_report(self) -> Dict[str, Any]:
        """获取综合报告"""
        return {
            'current_stats': self.get_current_stats(),
            'system_metrics': self.get_system_metrics(),
            'error_summary': self.get_error_summary(),
            'performance_summary': self.get_performance_summary(),
            'database_stats': self.get_database_stats(),
            'monitoring_status': {
                'active': self.monitoring_active,
                'uptime': time.time() - (self.current_metrics.timestamp.timestamp() if self.current_metrics.timestamp else time.time())
            }
        }
    
    def _save_stats_history(self):
        """保存统计历史到文件"""
        try:
            # 保存爬虫统计
            stats_data = {
                'stats_history': [stats.to_dict() for stats in list(self.stats_history)],
                'error_counts': dict(self.error_counts),
                'error_history': list(self.error_history)
            }
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, ensure_ascii=False, indent=2)
            
            # 保存系统指标
            metrics_data = {
                'metrics_history': [metrics.to_dict() for metrics in list(self.metrics_history)]
            }
            
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(metrics_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"保存统计历史失败: {str(e)}")
    
    def _load_stats_history(self):
        """从文件加载统计历史"""
        try:
            # 加载爬虫统计
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    stats_data = json.load(f)
                
                # 恢复统计历史
                for stats_dict in stats_data.get('stats_history', []):
                    stats = CrawlerStats(**stats_dict)
                    # 转换时间字符串为datetime对象
                    if stats_dict.get('start_time'):
                        stats.start_time = datetime.fromisoformat(stats_dict['start_time'])
                    if stats_dict.get('end_time'):
                        stats.end_time = datetime.fromisoformat(stats_dict['end_time'])
                    self.stats_history.append(stats)
                
                # 恢复错误统计
                self.error_counts.update(stats_data.get('error_counts', {}))
                self.error_history.extend(stats_data.get('error_history', []))
            
            # 加载系统指标
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    metrics_data = json.load(f)
                
                # 恢复指标历史
                for metrics_dict in metrics_data.get('metrics_history', []):
                    metrics = SystemMetrics(**metrics_dict)
                    if metrics_dict.get('timestamp'):
                        metrics.timestamp = datetime.fromisoformat(metrics_dict['timestamp'])
                    self.metrics_history.append(metrics)
                    
        except Exception as e:
            logger.error(f"加载统计历史失败: {str(e)}")
    
    def clear_history(self, days: int = 30):
        """清理历史数据"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        with self.lock:
            # 清理统计历史
            self.stats_history = deque(
                [stats for stats in self.stats_history 
                 if stats.start_time and stats.start_time > cutoff_date],
                maxlen=self.max_history_size
            )
            
            # 清理指标历史
            self.metrics_history = deque(
                [metrics for metrics in self.metrics_history 
                 if metrics.timestamp > cutoff_date],
                maxlen=self.max_history_size
            )
            
            # 清理错误历史
            self.error_history = deque(
                [error for error in self.error_history 
                 if datetime.fromisoformat(error['timestamp']) > cutoff_date],
                maxlen=100
            )
        
        # 保存清理后的数据
        self._save_stats_history()
        logger.info(f"已清理 {days} 天前的历史数据")