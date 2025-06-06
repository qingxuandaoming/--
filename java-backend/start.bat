@echo off
echo Starting Java Backend Service...

REM Set JAVA_HOME
set JAVA_HOME=C:\PROGRA~1\Java\jdk-23
set PATH=%JAVA_HOME%\bin;%PATH%

echo JAVA_HOME: %JAVA_HOME%

REM Check Java version
java -version

REM Check Maven version
mvn -version

REM Clean and compile the project
echo Cleaning and compiling project...
mvn clean compile

REM Start Spring Boot application
echo Starting Spring Boot application...
mvn spring-boot:run

pause