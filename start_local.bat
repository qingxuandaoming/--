@echo off
chcp 65001 >nul
echo =======================================================
echo     灵境行者 (Spirit Journey Rider) - 本地一键启动
echo =======================================================
echo.
echo 提示：此脚本将在本地直接启动各个服务，不依赖 Docker。
echo 请确保您的电脑已安装：Java (JDK 17+)、Python 3、Node.js 以及 MySQL。
echo 并且 MySQL 数据库已经在 localhost:3306 运行。
echo.
pause

echo [1/3] 正在启动 Java 后端服务...
start "Java Backend (Spring Boot)" cmd /c "cd /d %~dp0java-backend && echo 正在启动 Java 后端... && mvn spring-boot:run || echo [错误] Java 后端启动失败，请检查 Maven 和 JDK 配置。 && pause"

echo [2/3] 正在启动 Python 爬虫服务...
start "Python Backend (Flask)" cmd /c "cd /d %~dp0python-backend && echo 正在安装 Python 依赖... && pip install -r requirements.txt && echo 正在启动 Python 后端... && python app.py || echo [错误] Python 后端启动失败，请检查 Python 环境。 && pause"

echo [3/3] 正在启动 Vue 前端服务...
start "Vue Frontend" cmd /c "cd /d %~dp0vue-cycling-app && echo 正在安装 Node 依赖... && npm install && echo 正在启动 Vue 前端... && npm run dev || echo [错误] Vue 前端启动失败，请检查 Node.js 环境。 && pause"

echo.
echo =======================================================
echo 所有启动指令已发送，请查看弹出的 3 个命令行窗口日志！
echo =======================================================
echo.
echo 稍后您可以在浏览器中访问：
echo 前端页面：http://localhost:5173
echo.
echo （如果需要停止服务，请直接关闭弹出的对应窗口即可）
echo.
pause
