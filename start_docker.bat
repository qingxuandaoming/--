@echo off
echo =======================================================
echo Spirit Journey Rider - Docker Quick Start
echo =======================================================
echo.

:: 检查 Docker 是否已安装并运行
docker --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker is not installed or not running.
    echo Please make sure Docker Desktop is OPEN and RUNNING in your system tray.
    echo Download: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

:: 检测 docker-compose 命令版本（兼容新旧版 Docker）
docker-compose --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    docker compose version >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] docker-compose not found.
        pause
        exit /b 1
    ) else (
        set COMPOSE_CMD=docker compose
    )
) else (
    set COMPOSE_CMD=docker-compose
)

:: 检查必需的初始化 SQL 文件是否存在
if not exist "%~dp0database\complete_init.sql" (
    echo [WARN] 未找到 %~dp0database\complete_init.sql
    echo   Docker 首次启动时可能无法自动初始化数据库。
    echo   请确认 database/complete_init.sql 文件存在后重试。
    pause
    exit /b 1
)

echo [INFO] Building and starting all services...
echo [INFO] This may take several minutes on first run...
%COMPOSE_CMD% -p cycling_system up -d --build --remove-orphans

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Docker 服务启动失败，请检查上方错误信息。
    echo   常见问题：
    echo   1. 端口 3307/8080/5000/80 被占用
    echo   2. database\complete_init.sql 缺失
    echo   3. Docker 守护进程未正常运行
    echo.
    echo 查看详细日志: %COMPOSE_CMD% -p cycling_system logs
    pause
    exit /b 1
)

:: 等待后端服务健康就绪
echo.
echo [INFO] Waiting for services to become healthy...
set /a WAIT=0

:health_loop
ping 127.0.0.1 -n 4 >nul
set /a WAIT+=3

:: 检查 Java 后端
curl -sf http://localhost:8080/api/route/health >nul 2>&1
set JAVA_OK=%ERRORLEVEL%

:: 检查 Python 后端
curl -sf http://localhost:5000/api/health >nul 2>&1
set PYTHON_OK=%ERRORLEVEL%

if %JAVA_OK% equ 0 (
    if %PYTHON_OK% equ 0 (
        echo [OK] All backends are healthy after %WAIT%s.
        goto :all_ready
    )
)

if %WAIT% lss 120 (
    echo [INFO] Still waiting... (%WAIT%s elapsed, Java=%JAVA_OK% Python=%PYTHON_OK%)
    goto :health_loop
)

echo [WARN] Backends did not respond within 120s. Check logs:
echo   %COMPOSE_CMD% -p cycling_system logs java-backend
echo   %COMPOSE_CMD% -p cycling_system logs python-backend

:all_ready

echo.
echo =======================================================
echo                     SUCCESS
echo =======================================================
echo.
echo Frontend: http://localhost
echo Java Backend: http://localhost:8080/api/route/health
echo Python Backend: http://localhost:5000/api/health
echo.
echo Default Admin: root / 123456
echo.
echo Logs: %COMPOSE_CMD% -p cycling_system logs -f
echo Stop: %COMPOSE_CMD% -p cycling_system down
echo =======================================================
pause
