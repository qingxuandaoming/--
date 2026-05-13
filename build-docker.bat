@echo off
chcp 65001 >nul
echo ============================================================
echo   骑行装备数据分析系统 - Docker 一键构建脚本
echo ============================================================
echo.

:: 检查 Docker
docker --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker 未安装或未运行。
    echo 请确保 Docker Desktop 已启动。
    pause
    exit /b 1
)

:: 检查 docker-compose 或 docker compose
docker-compose --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    docker compose version >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] docker-compose / docker compose 未找到。
        pause
        exit /b 1
    ) else (
        set COMPOSE_CMD=docker compose
    )
) else (
    set COMPOSE_CMD=docker-compose
)

echo [INFO] 使用命令: %COMPOSE_CMD%
echo.

:: 构建镜像
echo [Step 1/3] 构建 Docker 镜像...
%COMPOSE_CMD% -p cycling_system build --no-cache
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker 镜像构建失败。
    pause
    exit /b 1
)
echo   镜像构建成功
echo.

:: 启动服务
echo [Step 2/3] 启动服务...
%COMPOSE_CMD% -p cycling_system up -d
if %ERRORLEVEL% neq 0 (
    echo [ERROR] 服务启动失败。
    pause
    exit /b 1
)
echo   服务已启动
echo.

:: 等待并显示状态
echo [Step 3/3] 检查服务状态...
timeout /t 5 /nobreak >nul
%COMPOSE_CMD% -p cycling_system ps
echo.

:: 显示访问信息
echo ============================================================
echo   Docker 部署完成！
echo ============================================================
echo.
echo   前端访问: http://localhost
echo   Java API: http://localhost:8080/api/route/health
echo   Python API: http://localhost:5000/api/health
echo.
echo   常用命令:
echo     查看日志: %COMPOSE_CMD% -p cycling_system logs -f
echo     停止服务: %COMPOSE_CMD% -p cycling_system down
echo     重启服务: %COMPOSE_CMD% -p cycling_system restart
echo ============================================================
pause
