@echo off
echo =======================================================
echo Spirit Journey Rider - Docker Quick Start
echo =======================================================
echo.

docker --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker is not installed or not running.
    echo Download: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

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

echo [INFO] Building and starting all services...
%COMPOSE_CMD% up -d --build

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
echo Logs: %COMPOSE_CMD% logs -f
echo Stop: %COMPOSE_CMD% down
echo =======================================================
pause
