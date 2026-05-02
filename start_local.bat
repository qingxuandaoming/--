@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo Starting Spirit Journey Rider Locally
echo ==========================================
echo.

:: Auto-detect Java (multi-source)
set "JAVA_CMD="

:: 1. Check JAVA_HOME
if defined JAVA_HOME (
    if exist "%JAVA_HOME%\bin\java.exe" (
        set "JAVA_CMD=%JAVA_HOME%\bin\java.exe"
        echo [OK] Found Java via JAVA_HOME.
    )
)

:: 2. Check common IDE auto-download folders (Trae/IntelliJ)
if not defined JAVA_CMD (
    for /d %%d in ("%USERPROFILE%\.jdks\temurin-24*" "%USERPROFILE%\.jdks\temurin-23*" "%USERPROFILE%\.jdks\temurin-21*" "%USERPROFILE%\.jdks\temurin-17*" "%USERPROFILE%\.jdks\*-24*" "%USERPROFILE%\.jdks\*-23*" "%USERPROFILE%\.jdks\*-21*" "%USERPROFILE%\.jdks\*-17*") do (
        if exist "%%d\bin\java.exe" (
            if not defined JAVA_CMD (
                set "JAVA_CMD=%%d\bin\java.exe"
                echo [OK] Found Java in IDE folder: %%d
            )
        )
    )
)

:: 3. Check common install paths
if not defined JAVA_CMD (
    for %%p in (
        "C:\Program Files\Java\jdk-24"
        "C:\Program Files\Java\jdk-23"
        "C:\Program Files\Java\jdk-21"
        "C:\Program Files\Java\jdk-17"
        "C:\Program Files\Eclipse Adoptium\jdk-24*"
        "C:\Program Files\Eclipse Adoptium\jdk-23*"
        "C:\Program Files\Eclipse Adoptium\jdk-21*"
        "C:\Program Files\Eclipse Adoptium\jdk-17*"
        "C:\PROGRA~1\Java\jdk-23"
        "C:\PROGRA~1\Java\jdk-24"
        "E:\application\java-1.8.0-openjdk-1.8.0.492.b09-1.win.jdk.x86_64"
    ) do (
        for /d %%d in ("%%~p") do (
            if exist "%%d\bin\java.exe" (
                if not defined JAVA_CMD (
                    set "JAVA_CMD=%%d\bin\java.exe"
                    echo [OK] Found Java in common path: %%d
                )
            )
        )
    )
)

:: 4. Fallback to PATH
if not defined JAVA_CMD (
    for /f "delims=" %%p in ('where java.exe 2^>nul') do (
        set "JAVA_CMD=%%p"
        echo [OK] Found Java in PATH.
        goto :java_found
    )
)
:java_found
if not defined JAVA_CMD (
    echo [ERROR] Java not found!
    echo.
    echo Please install JDK 17+ or set JAVA_HOME environment variable.
    echo.
    pause
    exit /b 1
)
echo [INFO] Using: %JAVA_CMD%
"%JAVA_CMD%" -version 2^>^&1 | findstr /i "version"
echo.

:: ============================================================
:: Check required files/directories
:: ============================================================

if not exist "%~dp0java-backend\target\cycling-route-backend-1.0.0.jar" (
    echo [ERROR] Java backend JAR not found!
    echo          Path: %~dp0java-backend\target\cycling-route-backend-1.0.0.jar
    echo          Please build the Java backend first.
    pause
    exit /b 1
)

if not exist "%~dp0python-backend\.venv\Scripts\python.exe" (
    echo [ERROR] Python virtual env not found!
    echo          Path: %~dp0python-backend\.venv\Scripts\python.exe
    echo          Please create .venv in python-backend directory first.
    pause
    exit /b 1
)

if not exist "%~dp0vue-cycling-app\node_modules" (
    echo [ERROR] Frontend dependencies not found!
    echo          Please run 'npm install' in vue-cycling-app directory first.
    pause
    exit /b 1
)

:: ============================================================
:: Detect / free backend ports
:: ============================================================

echo [INFO] Checking backend ports...

:: Free Java port 8080
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080 " ^| findstr "LISTENING"') do (
    echo [WARN] Port 8080 is in use by PID %%a. Stopping it...
    taskkill /F /PID %%a >nul 2>&1
    timeout /t 1 /nobreak >nul
)

:: Free Python port 5000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000 " ^| findstr "LISTENING"') do (
    echo [WARN] Port 5000 is in use by PID %%a. Stopping it...
    taskkill /F /PID %%a >nul 2>&1
    timeout /t 1 /nobreak >nul
)

:: ============================================================
:: Detect frontend port (5500 -> 5510 -> 5520)
:: ============================================================

set "FRONTEND_PORT="
for %%p in (5500 5510 5520) do (
    netstat -ano | findstr "LISTENING" | findstr ":%%p " >nul 2>&1
    if errorlevel 1 (
        set "FRONTEND_PORT=%%p"
        echo [OK] Frontend port %%p is available.
        goto :port_found
    ) else (
        echo [WARN] Port %%p is in use, trying next...
    )
)

echo [ERROR] All ports (5500, 5510, 5520) are in use! Please free one and retry.
pause
exit /b 1

:port_found
echo.

:: ============================================================
:: [1/3] Start Java Backend
:: ============================================================

echo [1/3] Starting Java Backend...
start /MIN "Java Backend" cmd /c ""%~dp0java-backend\start.bat" "%JAVA_CMD%""

:: Wait and verify
set /a RETRY=0
:java_wait
 timeout /t 1 /nobreak >nul
 netstat -ano | findstr "LISTENING" | findstr ":8080 " >nul 2>&1
 if not errorlevel 1 goto :java_ok
 set /a RETRY+=1
 if !RETRY! lss 30 goto :java_wait
 echo [ERROR] Java backend failed to start on port 8080 within 30 seconds.
 echo         Log file: %~dp0java_logs.txt
 pause
 exit /b 1
:java_ok
echo [OK] Java backend started. Log: %~dp0java_logs.txt

:: ============================================================
:: [2/3] Start Python Backend
:: ============================================================

echo [2/3] Starting Python Backend (with scheduler)...
start /MIN "Python Backend" cmd /c ""%~dp0python-backend\start.bat""

:: Wait and verify
set /a RETRY=0
:python_wait
 timeout /t 1 /nobreak >nul
 netstat -ano | findstr "LISTENING" | findstr ":5000 " >nul 2>&1
 if not errorlevel 1 goto :python_ok
 set /a RETRY+=1
 if !RETRY! lss 20 goto :python_wait
 echo [ERROR] Python backend failed to start on port 5000 within 20 seconds.
 echo         Log file: %~dp0python_logs.txt
 pause
 exit /b 1
:python_ok
echo [OK] Python backend started. Log: %~dp0python_logs.txt

:: ============================================================
:: [3/3] Start Vue Frontend
:: ============================================================

echo [3/3] Starting Vue Frontend (Vite) on port %FRONTEND_PORT%...
echo.
echo ==========================================
echo   Frontend URL: http://localhost:%FRONTEND_PORT%
echo   Java API:     http://localhost:8080/api
echo   Python API:   http://localhost:5000/api
echo ==========================================
echo.
echo Press Ctrl+C to stop all services.
echo.

start /WAIT "Vue Frontend" cmd /c ""%~dp0vue-cycling-app\start.bat" %FRONTEND_PORT%"

:: ============================================================
:: Cleanup: stop backends when frontend exits
:: ============================================================

echo.
echo [INFO] Stopping backend services...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080 " ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
    echo [OK] Java backend stopped.
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5000 " ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
    echo [OK] Python backend stopped.
)

echo.
echo All services stopped.
pause
