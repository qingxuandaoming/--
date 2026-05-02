@echo off
set "JAVA_HOME=E:\project\灵境行者\src\dist\骑行装备数据分析系统\runtime\jre"
set "PATH=%JAVA_HOME%\bin;%PATH%"
echo Java Version:
java -version
echo.
echo Starting Spring Boot application...
java -jar target\cycling-route-backend-1.0.0.jar
pause
