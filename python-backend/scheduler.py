from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from loguru import logger
import os
from services.crawler_service import CrawlerService
from services.equipment_service import EquipmentService
from app import app, db

class TaskScheduler:
    """任务调度器"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.crawler_service = CrawlerService()
        self.equipment_service = EquipmentService()
        self._setup_jobs()
    
    def _setup_jobs(self):
        """设置定时任务"""
        
        # 每天凌晨2点执行全量爬虫
        self.scheduler.add_job(
            func=self.daily_full_crawl,
            trigger=CronTrigger(hour=2, minute=0),
            id='daily_full_crawl',
            name='每日全量爬虫',
            replace_existing=True
        )
        
        # 每4小时执行热门商品价格更新
        self.scheduler.add_job(
            func=self.update_popular_prices,
            trigger=CronTrigger(hour='*/4'),
            id='update_popular_prices',
            name='热门商品价格更新',
            replace_existing=True
        )
        
        # 每小时清理过期任务
        self.scheduler.add_job(
            func=self.cleanup_tasks,
            trigger=CronTrigger(minute=0),
            id='cleanup_tasks',
            name='清理过期任务',
            replace_existing=True
        )
        
        # 每天凌晨3点更新装备评分
        self.scheduler.add_job(
            func=self.update_equipment_ratings,
            trigger=CronTrigger(hour=3, minute=0),
            id='update_equipment_ratings',
            name='更新装备评分',
            replace_existing=True
        )
        
        # 每30分钟检查价格提醒
        self.scheduler.add_job(
            func=self.check_price_alerts,
            trigger=CronTrigger(minute='*/30'),
            id='check_price_alerts',
            name='检查价格提醒',
            replace_existing=True
        )
    
    def daily_full_crawl(self):
        """每日全量爬虫任务"""
        try:
            logger.info("开始执行每日全量爬虫任务")
            
            with app.app_context():
                # 爬取所有分类的装备
                task_id = self.crawler_service.start_crawl_task('all', 'all')
                logger.info(f"全量爬虫任务已启动，任务ID: {task_id}")
                
        except Exception as e:
            logger.error(f"每日全量爬虫任务执行失败: {str(e)}")
    
    def update_popular_prices(self):
        """更新热门商品价格"""
        try:
            logger.info("开始更新热门商品价格")
            
            with app.app_context():
                # 获取热门装备（评分高、评价多的商品）
                popular_equipment = self.equipment_service.get_popular_equipment(limit=50)
                
                # 为热门装备启动价格更新爬虫
                for equipment in popular_equipment:
                    try:
                        # 这里可以实现针对特定商品的价格更新逻辑
                        logger.info(f"更新装备价格: {equipment['name']}")
                    except Exception as e:
                        logger.error(f"更新装备 {equipment['id']} 价格失败: {str(e)}")
                        continue
                
                logger.info(f"热门商品价格更新完成，共处理 {len(popular_equipment)} 个商品")
                
        except Exception as e:
            logger.error(f"更新热门商品价格失败: {str(e)}")
    
    def cleanup_tasks(self):
        """清理过期任务"""
        try:
            logger.info("开始清理过期任务")
            
            # 清理7天前的爬虫任务记录
            self.crawler_service.cleanup_old_tasks(days=7)
            
            logger.info("过期任务清理完成")
            
        except Exception as e:
            logger.error(f"清理过期任务失败: {str(e)}")
    
    def update_equipment_ratings(self):
        """更新装备评分"""
        try:
            logger.info("开始更新装备评分")
            
            with app.app_context():
                # 获取所有活跃装备
                from models.equipment import Equipment
                equipment_list = Equipment.query.filter(
                    Equipment.is_active == True
                ).all()
                
                updated_count = 0
                for equipment in equipment_list:
                    try:
                        self.equipment_service.update_equipment_rating(equipment.id)
                        updated_count += 1
                    except Exception as e:
                        logger.error(f"更新装备 {equipment.id} 评分失败: {str(e)}")
                        continue
                
                logger.info(f"装备评分更新完成，共更新 {updated_count} 个装备")
                
        except Exception as e:
            logger.error(f"更新装备评分失败: {str(e)}")
    
    def check_price_alerts(self):
        """检查价格提醒"""
        try:
            logger.info("开始检查价格提醒")
            
            with app.app_context():
                # 这里实现价格提醒检查逻辑
                # 1. 获取所有活跃的价格提醒
                # 2. 检查当前价格是否达到目标价格
                # 3. 发送提醒通知
                
                from sqlalchemy import text
                
                # 查询需要检查的价格提醒
                query = text("""
                    SELECT pa.*, e.name as equipment_name, u.email as user_email
                    FROM price_alerts pa
                    JOIN equipment e ON pa.equipment_id = e.id
                    JOIN users u ON pa.user_id = u.id
                    WHERE pa.is_active = 1
                    AND (pa.last_check_time IS NULL OR pa.last_check_time < DATE_SUB(NOW(), INTERVAL 1 HOUR))
                """)
                
                alerts = db.session.execute(query).fetchall()
                
                checked_count = 0
                triggered_count = 0
                
                for alert in alerts:
                    try:
                        # 获取当前最低价格
                        current_prices = self.equipment_service.get_latest_prices(
                            alert.equipment_id, limit=10
                        )
                        
                        if current_prices:
                            min_price = min(price['price'] for price in current_prices 
                                           if price['is_available'])
                            
                            # 检查是否达到目标价格
                            if min_price <= float(alert.target_price):
                                # 发送价格提醒
                                self._send_price_alert(alert, min_price)
                                triggered_count += 1
                        
                        # 更新最后检查时间
                        update_query = text("""
                            UPDATE price_alerts 
                            SET last_check_time = NOW() 
                            WHERE id = :alert_id
                        """)
                        db.session.execute(update_query, {'alert_id': alert.id})
                        
                        checked_count += 1
                        
                    except Exception as e:
                        logger.error(f"检查价格提醒 {alert.id} 失败: {str(e)}")
                        continue
                
                db.session.commit()
                
                logger.info(f"价格提醒检查完成，共检查 {checked_count} 个提醒，触发 {triggered_count} 个")
                
        except Exception as e:
            logger.error(f"检查价格提醒失败: {str(e)}")
    
    def _send_price_alert(self, alert, current_price):
        """发送价格提醒"""
        try:
            # 这里实现发送邮件或其他通知方式
            logger.info(
                f"价格提醒触发: 用户 {alert.user_email}, "
                f"商品 {alert.equipment_name}, "
                f"目标价格 ¥{alert.target_price}, "
                f"当前价格 ¥{current_price}"
            )
            
            # TODO: 实现邮件发送或推送通知
            
        except Exception as e:
            logger.error(f"发送价格提醒失败: {str(e)}")
    
    def start(self):
        """启动调度器"""
        try:
            self.scheduler.start()
            logger.info("任务调度器已启动")
            
            # 打印所有已注册的任务
            jobs = self.scheduler.get_jobs()
            logger.info(f"已注册 {len(jobs)} 个定时任务:")
            for job in jobs:
                logger.info(f"  - {job.name} (ID: {job.id})")
                
        except Exception as e:
            logger.error(f"启动任务调度器失败: {str(e)}")
    
    def stop(self):
        """停止调度器"""
        try:
            self.scheduler.shutdown()
            logger.info("任务调度器已停止")
        except Exception as e:
            logger.error(f"停止任务调度器失败: {str(e)}")
    
    def get_job_status(self):
        """获取任务状态"""
        jobs = self.scheduler.get_jobs()
        job_status = []
        
        for job in jobs:
            job_info = {
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            }
            job_status.append(job_info)
        
        return {
            'scheduler_running': self.scheduler.running,
            'total_jobs': len(jobs),
            'jobs': job_status
        }

if __name__ == '__main__':
    # 独立运行调度器
    scheduler = TaskScheduler()
    
    try:
        scheduler.start()
        logger.info("调度器已启动，按 Ctrl+C 停止")
        
        # 保持程序运行
        import time
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("收到停止信号")
        scheduler.stop()