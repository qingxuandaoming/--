#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署脚本
用于快速部署和管理Python后端服务
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path
from loguru import logger

class DeployManager:
    """部署管理器"""
    
    def __init__(self, project_dir=None):
        self.project_dir = Path(project_dir or os.getcwd())
        self.docker_compose_file = self.project_dir / 'docker-compose.yml'
        self.env_file = self.project_dir / '.env'
        
    def check_requirements(self):
        """检查部署要求"""
        logger.info("检查部署要求...")
        
        # 检查Docker
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, check=True)
            logger.success(f"Docker已安装: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("Docker未安装或不可用")
            return False
        
        # 检查Docker Compose
        try:
            result = subprocess.run(['docker-compose', '--version'], 
                                  capture_output=True, text=True, check=True)
            logger.success(f"Docker Compose已安装: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("Docker Compose未安装或不可用")
            return False
        
        # 检查配置文件
        if not self.docker_compose_file.exists():
            logger.error(f"Docker Compose配置文件不存在: {self.docker_compose_file}")
            return False
        
        logger.success("部署要求检查通过")
        return True
    
    def setup_environment(self):
        """设置环境配置"""
        logger.info("设置环境配置...")
        
        if not self.env_file.exists():
            env_example = self.project_dir / '.env.example'
            if env_example.exists():
                logger.info("复制环境配置模板...")
                with open(env_example, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                with open(self.env_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                logger.warning("请编辑 .env 文件配置相关参数")
            else:
                logger.error("环境配置模板文件不存在")
                return False
        
        logger.success("环境配置已设置")
        return True
    
    def build_images(self):
        """构建Docker镜像"""
        logger.info("构建Docker镜像...")
        
        try:
            cmd = ['docker-compose', 'build', '--no-cache']
            result = subprocess.run(cmd, cwd=self.project_dir, check=True)
            logger.success("Docker镜像构建完成")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Docker镜像构建失败: {e}")
            return False
    
    def start_services(self, detached=True):
        """启动服务"""
        logger.info("启动服务...")
        
        try:
            cmd = ['docker-compose', 'up']
            if detached:
                cmd.append('-d')
            
            result = subprocess.run(cmd, cwd=self.project_dir, check=True)
            
            if detached:
                logger.success("服务已在后台启动")
                self.show_status()
            else:
                logger.success("服务启动完成")
            
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"服务启动失败: {e}")
            return False
    
    def stop_services(self):
        """停止服务"""
        logger.info("停止服务...")
        
        try:
            cmd = ['docker-compose', 'down']
            result = subprocess.run(cmd, cwd=self.project_dir, check=True)
            logger.success("服务已停止")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"服务停止失败: {e}")
            return False
    
    def restart_services(self):
        """重启服务"""
        logger.info("重启服务...")
        
        if self.stop_services():
            time.sleep(2)
            return self.start_services()
        return False
    
    def show_status(self):
        """显示服务状态"""
        logger.info("服务状态:")
        
        try:
            cmd = ['docker-compose', 'ps']
            result = subprocess.run(cmd, cwd=self.project_dir, 
                                  capture_output=True, text=True, check=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"获取服务状态失败: {e}")
    
    def show_logs(self, service=None, follow=False, tail=100):
        """显示服务日志"""
        logger.info(f"显示服务日志 {'(实时)' if follow else ''}...")
        
        try:
            cmd = ['docker-compose', 'logs']
            
            if follow:
                cmd.append('-f')
            
            if tail:
                cmd.extend(['--tail', str(tail)])
            
            if service:
                cmd.append(service)
            
            subprocess.run(cmd, cwd=self.project_dir, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"获取日志失败: {e}")
        except KeyboardInterrupt:
            logger.info("停止日志显示")
    
    def cleanup(self):
        """清理资源"""
        logger.info("清理Docker资源...")
        
        try:
            # 停止并删除容器
            cmd = ['docker-compose', 'down', '-v', '--remove-orphans']
            subprocess.run(cmd, cwd=self.project_dir, check=True)
            
            # 删除未使用的镜像
            cmd = ['docker', 'image', 'prune', '-f']
            subprocess.run(cmd, check=True)
            
            logger.success("资源清理完成")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"资源清理失败: {e}")
            return False
    
    def backup_database(self, backup_dir='./backups'):
        """备份数据库"""
        logger.info("备份数据库...")
        
        backup_path = Path(backup_dir)
        backup_path.mkdir(exist_ok=True)
        
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        backup_file = backup_path / f'ljxz_backup_{timestamp}.sql'
        
        try:
            cmd = [
                'docker-compose', 'exec', '-T', 'mysql',
                'mysqldump', '-u', 'ljxz_user', '-pljxz_pass', 'ljxz'
            ]
            
            with open(backup_file, 'w') as f:
                result = subprocess.run(cmd, cwd=self.project_dir, 
                                      stdout=f, check=True)
            
            logger.success(f"数据库备份完成: {backup_file}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"数据库备份失败: {e}")
            return False
    
    def deploy(self, build=True):
        """完整部署流程"""
        logger.info("开始部署流程...")
        
        steps = [
            ("检查部署要求", self.check_requirements),
            ("设置环境配置", self.setup_environment),
        ]
        
        if build:
            steps.append(("构建Docker镜像", self.build_images))
        
        steps.append(("启动服务", lambda: self.start_services(detached=True)))
        
        for step_name, step_func in steps:
            logger.info(f"执行步骤: {step_name}")
            
            if not step_func():
                logger.error(f"步骤失败: {step_name}")
                return False
            
            logger.success(f"步骤完成: {step_name}")
        
        logger.success("部署完成！")
        
        # 显示访问信息
        logger.info("服务访问信息:")
        logger.info("  - API服务: http://localhost:5000")
        logger.info("  - 健康检查: http://localhost:5000/api/health")
        logger.info("  - MySQL: localhost:3306")
        logger.info("  - Redis: localhost:6379")
        
        return True

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Python后端部署管理工具')
    parser.add_argument('--project-dir', help='项目目录路径')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 部署命令
    deploy_parser = subparsers.add_parser('deploy', help='完整部署')
    deploy_parser.add_argument('--no-build', action='store_true', help='跳过镜像构建')
    
    # 构建命令
    subparsers.add_parser('build', help='构建Docker镜像')
    
    # 启动命令
    start_parser = subparsers.add_parser('start', help='启动服务')
    start_parser.add_argument('--foreground', action='store_true', help='前台运行')
    
    # 停止命令
    subparsers.add_parser('stop', help='停止服务')
    
    # 重启命令
    subparsers.add_parser('restart', help='重启服务')
    
    # 状态命令
    subparsers.add_parser('status', help='显示服务状态')
    
    # 日志命令
    logs_parser = subparsers.add_parser('logs', help='显示服务日志')
    logs_parser.add_argument('--service', help='指定服务名称')
    logs_parser.add_argument('--follow', '-f', action='store_true', help='实时跟踪日志')
    logs_parser.add_argument('--tail', type=int, default=100, help='显示最后N行日志')
    
    # 清理命令
    subparsers.add_parser('cleanup', help='清理Docker资源')
    
    # 备份命令
    backup_parser = subparsers.add_parser('backup', help='备份数据库')
    backup_parser.add_argument('--dir', default='./backups', help='备份目录')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = DeployManager(args.project_dir)
    
    try:
        if args.command == 'deploy':
            manager.deploy(build=not args.no_build)
        elif args.command == 'build':
            manager.build_images()
        elif args.command == 'start':
            manager.start_services(detached=not args.foreground)
        elif args.command == 'stop':
            manager.stop_services()
        elif args.command == 'restart':
            manager.restart_services()
        elif args.command == 'status':
            manager.show_status()
        elif args.command == 'logs':
            manager.show_logs(args.service, args.follow, args.tail)
        elif args.command == 'cleanup':
            manager.cleanup()
        elif args.command == 'backup':
            manager.backup_database(args.dir)
    
    except KeyboardInterrupt:
        logger.info("操作被用户中断")
    except Exception as e:
        logger.error(f"操作失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()