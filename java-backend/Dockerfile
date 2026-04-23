# 使用 Maven 镜像进行构建阶段
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app

# 为了避免每次修改代码都重新下载依赖，先只复制 pom.xml
COPY pom.xml .

# 修改 pom.xml 的 java 版本到 21，因为 maven docker image 可能不自带 23 或者为了稳定
RUN sed -i 's/<source>23<\/source>/<source>21<\/source>/g' pom.xml && \
    sed -i 's/<target>23<\/target>/<target>21<\/target>/g' pom.xml && \
    sed -i 's/<maven.compiler.source>23<\/maven.compiler.source>/<maven.compiler.source>21<\/maven.compiler.source>/g' pom.xml && \
    sed -i 's/<maven.compiler.target>23<\/maven.compiler.target>/<maven.compiler.target>21<\/maven.compiler.target>/g' pom.xml

# 下载依赖 (可选, 加速后续构建)
RUN mvn dependency:go-offline -B

# 复制源代码并构建
COPY src ./src
RUN mvn clean package -DskipTests

# 使用轻量级 JRE 镜像运行
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# 从构建阶段复制 jar 文件
COPY --from=build /app/target/cycling-route-backend-1.0.0.jar app.jar

# 暴露端口
EXPOSE 8080

# 运行应用
ENTRYPOINT ["java", "-jar", "app.jar"]
