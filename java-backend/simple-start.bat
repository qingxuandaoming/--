@echo off
setlocal enabledelayedexpansion

:: ×Ô¶¯¼ì²â JAVA_HOME
set "JAVA_HOME_FOUND="
if defined JAVA_HOME (
    if exist "%JAVA_HOME%\bin\java.exe" (
        set "JAVA_HOME_FOUND=%JAVA_HOME%"
    )
)
if not defined JAVA_HOME_FOUND (
    for /f "delims=" %%p in ('where java.exe 2^>nul') do (
        set "JAVA_HOME_FOUND=%%~dp"
        if "!JAVA_HOME_FOUND:~-1!"=="\" set "JAVA_HOME_FOUND=!JAVA_HOME_FOUND:~0,-1!"
        if "!JAVA_HOME_FOUND:~-4!"=="\bin" set "JAVA_HOME_FOUND=!JAVA_HOME_FOUND:~0,-4!"
        goto :java_ok
    )
)
:java_ok
if not defined JAVA_HOME_FOUND (
    echo [ERROR] Java not found! Please install JDK and set JAVA_HOME.
    pause
    exit /b 1
)
set "JAVA_HOME=%JAVA_HOME_FOUND%"
set "PATH=%JAVA_HOME%\bin;%PATH%"

echo Java Version:
java -version
echo.
echo Starting Spring Boot application...
java -jar target\cycling-route-backend-1.0.0.jar
pause
