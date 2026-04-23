@echo off
echo =======================================================
echo     灵境行者 (Spirit Journey Rider) - Docker 一键启动
echo =======================================================
echo.

REM 检查是否安装了 docker
docker --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [错误] 未检测到 Docker，请先安装 Docker Desktop 并确保其正在运行。
    echo 下载地址：https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

REM 检查 docker-compose 是否存在
docker-compose --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    docker compose version >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo [错误] 未检测到 docker-compose，请确保 Docker 已正确安装。
        pause
        exit /b 1
    ) else (
        set COMPOSE_CMD=docker compose
    )
) else (
    set COMPOSE_CMD=docker-compose
)

echo [信息] 正在构建并启动所有服务，首次启动可能需要一些时间下载依赖和镜像...
%COMPOSE_CMD% up -d --build

echo.
echo =======================================================
echo                     启动成功！
echo =======================================================
echo.
echo 前端访问地址: http://localhost
echo Java后端接口: http://localhost:8080/api/route/health
echo Python后端接口: http://localhost:5000/api/health
echo.
echo 默认管理账号: root / 123456
echo.
echo 如需查看日志，请运行: %COMPOSE_CMD% logs -f
echo 如需停止服务，请运行: %COMPOSE_CMD% down
echo =======================================================
pause
