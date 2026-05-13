import uuid
import time
import threading
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from queue import PriorityQueue, Queue, Empty
import json
import os
from concurrent.futures import ThreadPoolExecutor, Future
import logging

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"      # 等待中
    RUNNING = "running"      # 运行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 失败
    CANCELLED = "cancelled"  # 已取消
    PAUSED = "paused"        # 已暂停

class TaskPriority(Enum):
    """任务优先级枚举"""
    LOW = 3
    NORMAL = 2
    HIGH = 1
    URGENT = 0

@dataclass
class CrawlerTask:
    """爬虫任务数据类"""
    task_id: str
    task_type: str  # 'full_crawl', 'price_update', 'category_crawl', etc.
    platform: str
    category: str = ""
    keywords: List[str] = None
    max_items: int = 100
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float = 0.0
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    timeout: int = 3600  # 1小时超时
    dependencies: List[str] = None  # 依赖的任务ID
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.dependencies is None:
            self.dependencies = []
        if self.metadata is None:
            self.metadata = {}
    
    def __lt__(self, other):
        """用于优先级队列排序"""
        return self.priority.value < other.priority.value
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['priority'] = self.priority.name
        data['status'] = self.status.name
        data['created_at'] = self.created_at.isoformat() if self.created_at else None
        data['started_at'] = self.started_at.isoformat() if self.started_at else None
        data['completed_at'] = self.completed_at.isoformat() if self.completed_at else None
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CrawlerTask':
        """从字典创建任务"""
        # 转换枚举
        if 'priority' in data and isinstance(data['priority'], str):
            data['priority'] = TaskPriority[data['priority']]
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = TaskStatus[data['status']]
        
        # 转换时间
        for time_field in ['created_at', 'started_at', 'completed_at']:
            if data.get(time_field) and isinstance(data[time_field], str):
                data[time_field] = datetime.fromisoformat(data[time_field])
        
        return cls(**data)

class CrawlerQueueService:
    """爬虫任务队列服务"""
    
    def __init__(self, max_workers: int = 5, queue_file: str = 'crawler_queue.json'):
        self.max_workers = max_workers
        self.queue_file = queue_file
        
        # 任务队列和存储
        self.task_queue = PriorityQueue()
        self.tasks: Dict[str, CrawlerTask] = {}
        self.running_tasks: Dict[str, Future] = {}
        
        # 线程池
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
        # 任务处理器注册
        self.task_handlers: Dict[str, Callable] = {}
        
        # 控制标志
        self.is_running = False
        self.worker_thread = None
        self.lock = threading.Lock()
        
        # 统计信息
        self.stats = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'failed_tasks': 0,
            'cancelled_tasks': 0,
            'avg_execution_time': 0.0
        }
        
        # 加载持久化的任务
        self._load_tasks()
    
    def register_handler(self, task_type: str, handler: Callable):
        """注册任务处理器"""
        self.task_handlers[task_type] = handler
        logger.info(f"注册任务处理器: {task_type}")
    
    def start(self):
        """启动队列服务"""
        if not self.is_running:
            self.is_running = True
            self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
            self.worker_thread.start()
            logger.info(f"爬虫队列服务已启动，最大工作线程数: {self.max_workers}")
    
    def stop(self):
        """停止队列服务"""
        self.is_running = False
        
        # 等待工作线程结束
        if self.worker_thread:
            self.worker_thread.join(timeout=10)
        
        # 取消所有运行中的任务
        with self.lock:
            for task_id, future in self.running_tasks.items():
                future.cancel()
                if task_id in self.tasks:
                    self.tasks[task_id].status = TaskStatus.CANCELLED
        
        # 关闭线程池
        self.executor.shutdown(wait=True)
        
        # 保存任务状态
        self._save_tasks()
        
        logger.info("爬虫队列服务已停止")
    
    def add_task(self, task: CrawlerTask) -> str:
        """添加任务到队列"""
        with self.lock:
            # 检查依赖任务
            if not self._check_dependencies(task):
                raise ValueError(f"任务依赖检查失败: {task.dependencies}")
            
            # 添加到队列和存储
            self.tasks[task.task_id] = task
            self.task_queue.put(task)
            self.stats['total_tasks'] += 1
            
            logger.info(f"添加任务到队列: {task.task_id} - {task.task_type}")
            
            # 保存到文件
            self._save_tasks()
            
            return task.task_id
    
    def create_task(self, task_type: str, platform: str, **kwargs) -> str:
        """创建并添加任务"""
        task_id = str(uuid.uuid4())
        
        task = CrawlerTask(
            task_id=task_id,
            task_type=task_type,
            platform=platform,
            **kwargs
        )
        
        return self.add_task(task)
    
    def get_task(self, task_id: str) -> Optional[CrawlerTask]:
        """获取任务信息"""
        with self.lock:
            return self.tasks.get(task_id)
    
    def get_tasks(self, status: Optional[TaskStatus] = None, 
                  task_type: Optional[str] = None,
                  platform: Optional[str] = None,
                  limit: int = 100) -> List[CrawlerTask]:
        """获取任务列表"""
        with self.lock:
            tasks = list(self.tasks.values())
            
            # 过滤条件
            if status:
                tasks = [t for t in tasks if t.status == status]
            if task_type:
                tasks = [t for t in tasks if t.task_type == task_type]
            if platform:
                tasks = [t for t in tasks if t.platform == platform]
            
            # 按创建时间排序
            tasks.sort(key=lambda t: t.created_at, reverse=True)
            
            return tasks[:limit]
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            
            # 如果任务正在运行，取消Future
            if task_id in self.running_tasks:
                future = self.running_tasks[task_id]
                future.cancel()
                del self.running_tasks[task_id]
            
            # 更新任务状态
            task.status = TaskStatus.CANCELLED
            task.completed_at = datetime.now()
            self.stats['cancelled_tasks'] += 1
            
            logger.info(f"任务已取消: {task_id}")
            self._save_tasks()
            
            return True
    
    def pause_task(self, task_id: str) -> bool:
        """暂停任务"""
        with self.lock:
            task = self.tasks.get(task_id)
            if not task or task.status != TaskStatus.PENDING:
                return False
            
            task.status = TaskStatus.PAUSED
            logger.info(f"任务已暂停: {task_id}")
            self._save_tasks()
            
            return True
    
    def resume_task(self, task_id: str) -> bool:
        """恢复任务"""
        with self.lock:
            task = self.tasks.get(task_id)
            if not task or task.status != TaskStatus.PAUSED:
                return False
            
            task.status = TaskStatus.PENDING
            self.task_queue.put(task)
            
            logger.info(f"任务已恢复: {task_id}")
            self._save_tasks()
            
            return True
    
    def retry_task(self, task_id: str) -> bool:
        """重试失败的任务"""
        with self.lock:
            task = self.tasks.get(task_id)
            if not task or task.status != TaskStatus.FAILED:
                return False
            
            if task.retry_count >= task.max_retries:
                logger.warning(f"任务重试次数已达上限: {task_id}")
                return False
            
            # 重置任务状态
            task.status = TaskStatus.PENDING
            task.retry_count += 1
            task.started_at = None
            task.completed_at = None
            task.progress = 0.0
            task.error_message = None
            
            # 重新加入队列
            self.task_queue.put(task)
            
            logger.info(f"任务重试: {task_id} (第{task.retry_count}次)")
            self._save_tasks()
            
            return True
    
    def get_queue_status(self) -> Dict[str, Any]:
        """获取队列状态"""
        with self.lock:
            pending_count = sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING)
            running_count = len(self.running_tasks)
            
            return {
                'is_running': self.is_running,
                'max_workers': self.max_workers,
                'queue_size': self.task_queue.qsize(),
                'pending_tasks': pending_count,
                'running_tasks': running_count,
                'total_tasks': len(self.tasks),
                'stats': self.stats.copy()
            }
    
    def clear_completed_tasks(self, days: int = 7):
        """清理已完成的任务"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        with self.lock:
            tasks_to_remove = []
            
            for task_id, task in self.tasks.items():
                if (task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED] and
                    task.completed_at and task.completed_at < cutoff_date):
                    tasks_to_remove.append(task_id)
            
            for task_id in tasks_to_remove:
                del self.tasks[task_id]
            
            logger.info(f"清理了 {len(tasks_to_remove)} 个已完成的任务")
            self._save_tasks()
            
            return len(tasks_to_remove)
    
    def _worker_loop(self):
        """工作线程循环"""
        while self.is_running:
            try:
                # 获取任务
                try:
                    task = self.task_queue.get(timeout=1)
                except Empty:
                    continue
                
                # 检查任务状态
                if task.status != TaskStatus.PENDING:
                    continue
                
                # 检查依赖
                if not self._are_dependencies_completed(task):
                    # 重新放回队列
                    self.task_queue.put(task)
                    time.sleep(1)
                    continue
                
                # 检查超时
                if self._is_task_timeout(task):
                    self._mark_task_failed(task, "任务超时")
                    continue
                
                # 提交任务执行
                future = self.executor.submit(self._execute_task, task)
                
                with self.lock:
                    self.running_tasks[task.task_id] = future
                    task.status = TaskStatus.RUNNING
                    task.started_at = datetime.now()
                
                # 设置完成回调
                future.add_done_callback(lambda f, tid=task.task_id: self._task_completed(tid, f))
                
            except Exception as e:
                logger.error(f"工作线程错误: {str(e)}")
                time.sleep(5)
    
    def _execute_task(self, task: CrawlerTask):
        """执行任务"""
        try:
            logger.info(f"开始执行任务: {task.task_id} - {task.task_type}")
            
            # 获取任务处理器
            handler = self.task_handlers.get(task.task_type)
            if not handler:
                raise ValueError(f"未找到任务处理器: {task.task_type}")
            
            # 执行任务
            result = handler(task)
            
            # 更新任务结果
            with self.lock:
                task.result = result
                task.progress = 100.0
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                
                # 更新统计
                self.stats['completed_tasks'] += 1
                if task.started_at:
                    execution_time = (task.completed_at - task.started_at).total_seconds()
                    self._update_avg_execution_time(execution_time)
            
            logger.info(f"任务执行完成: {task.task_id}")
            
        except Exception as e:
            logger.error(f"任务执行失败: {task.task_id} - {str(e)}")
            self._mark_task_failed(task, str(e))
    
    def _task_completed(self, task_id: str, future: Future):
        """任务完成回调"""
        with self.lock:
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]
        
        # 保存任务状态
        self._save_tasks()
    
    def _mark_task_failed(self, task: CrawlerTask, error_message: str):
        """标记任务失败"""
        with self.lock:
            task.status = TaskStatus.FAILED
            task.error_message = error_message
            task.completed_at = datetime.now()
            self.stats['failed_tasks'] += 1
    
    def _check_dependencies(self, task: CrawlerTask) -> bool:
        """检查任务依赖"""
        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                return False
        return True
    
    def _are_dependencies_completed(self, task: CrawlerTask) -> bool:
        """检查依赖任务是否已完成"""
        for dep_id in task.dependencies:
            dep_task = self.tasks.get(dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False
        return True
    
    def _is_task_timeout(self, task: CrawlerTask) -> bool:
        """检查任务是否超时"""
        if not task.started_at:
            return False
        
        elapsed = (datetime.now() - task.started_at).total_seconds()
        return elapsed > task.timeout
    
    def _update_avg_execution_time(self, execution_time: float):
        """更新平均执行时间"""
        completed = self.stats['completed_tasks']
        if completed == 1:
            self.stats['avg_execution_time'] = execution_time
        else:
            current_avg = self.stats['avg_execution_time']
            self.stats['avg_execution_time'] = (current_avg * (completed - 1) + execution_time) / completed
    
    def _save_tasks(self):
        """保存任务到文件"""
        try:
            tasks_data = {
                'tasks': {task_id: task.to_dict() for task_id, task in self.tasks.items()},
                'stats': self.stats
            }
            
            with open(self.queue_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"保存任务失败: {str(e)}")
    
    def _load_tasks(self):
        """从文件加载任务"""
        try:
            if os.path.exists(self.queue_file):
                with open(self.queue_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 恢复任务
                for task_id, task_data in data.get('tasks', {}).items():
                    task = CrawlerTask.from_dict(task_data)
                    self.tasks[task_id] = task
                    
                    # 将待处理的任务重新加入队列
                    if task.status == TaskStatus.PENDING:
                        self.task_queue.put(task)
                    elif task.status == TaskStatus.RUNNING:
                        # 将运行中的任务标记为失败（服务重启）
                        task.status = TaskStatus.FAILED
                        task.error_message = "服务重启，任务中断"
                        task.completed_at = datetime.now()
                
                # 恢复统计
                self.stats.update(data.get('stats', {}))
                
                logger.info(f"加载了 {len(self.tasks)} 个任务")
                
        except Exception as e:
            logger.error(f"加载任务失败: {str(e)}")