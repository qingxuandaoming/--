@echo off
set JAVA_HOME=C:\PROGRA~1\Java\jdk-23
set PATH=%JAVA_HOME%\bin;%PATH%
echo Starting Spring Boot application...
mvn spring-boot:run
pause