# 设置Java环境变量
$env:JAVA_HOME = 'C:\Program Files\Java\jdk-23'
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"

# 切换到Java后端目录
cd 'c:\Users\92534\Desktop\项目\灵境行者\site\java-backend'

# 启动Spring Boot应用
mvn org.springframework.boot:spring-boot-maven-plugin:run