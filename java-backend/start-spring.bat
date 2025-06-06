@echo off
set "JAVA_HOME=C:\Program Files\Java\jdk-23"
set "PATH=%JAVA_HOME%\bin;%PATH%"
echo Java Home: %JAVA_HOME%
echo Java Version:
java -version
echo Maven Version:
mvn -version
echo Starting Spring Boot Application...
mvn org.springframework.boot:spring-boot-maven-plugin:run