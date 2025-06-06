@echo off
cd /d "C:\Users\92534\Desktop\项目\灵境行者\site\java-backend"
set "JAVA_HOME=C:\PROGRA~1\Java\jdk-23"
set "PATH=%JAVA_HOME%\bin;%PATH%"
echo Starting Spring Boot application...
mvn spring-boot:run
pause