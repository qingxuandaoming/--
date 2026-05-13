@echo off
cd /d "%~dp0"

if not defined JAVA_HOME (
    set "JAVA_HOME=C:\PROGRA~1\Java\jdk-23"
)
if not exist "%JAVA_HOME%\bin\java.exe" (
    echo [ERROR] Java not found at %JAVA_HOME%
    pause
    exit /b 1
)
set "PATH=%JAVA_HOME%\bin;%PATH%"

echo Cleaning and compiling project...
mvn clean compile
echo.
echo Starting Spring Boot application...
mvn spring-boot:run
pause
