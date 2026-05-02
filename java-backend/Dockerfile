# 构建阶段：使用与项目 pom.xml 匹配的 Java 17 镜像
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app

# 先单独复制 pom.xml，利用 Docker 层缓存加速后续构建
COPY pom.xml .
RUN mvn dependency:go-offline -B

# 复制源代码并打包（跳过测试以加快构建）
COPY src ./src
RUN mvn clean package -DskipTests -B

# 运行阶段：使用轻量级 JRE 镜像
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# 安装 curl 用于健康检查
RUN apk add --no-cache curl

# 从构建阶段复制 jar 文件（使用通配符避免硬编码版本号）
COPY --from=build /app/target/*.jar app.jar

# 暴露端口
EXPOSE 8080

# 健康检查：给 Java 应用 60 秒启动时间
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=5 \
    CMD curl -f http://localhost:8080/api/route/health || exit 1

# 运行应用（使用推荐格式）
ENTRYPOINT ["java", "-jar", "app.jar"]
