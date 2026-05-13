@echo off
cd /d "%~dp0"

if not defined JAVA_HOME (
    set "JAVA_HOME=C:\Program Files\Java\jdk-23"
)
if not exist "%JAVA_HOME%\bin\java.exe" (
    echo [ERROR] Java not found at %JAVA_HOME%
    pause
    exit /b 1
)
set "PATH=%JAVA_HOME%\bin;%PATH%"

echo Java Home: %JAVA_HOME%
echo Java Version:
java -version
echo Maven Version:
mvn -version
echo Starting Spring Boot Application...
mvn org.springframework.boot:spring-boot-maven-plugin:run
