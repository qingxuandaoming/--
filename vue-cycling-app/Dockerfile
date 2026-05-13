# 构建阶段
FROM node:18-alpine AS build
WORKDIR /app

# 复制包描述文件并安装依赖（利用层缓存）
COPY package*.json ./
RUN npm install

# 复制项目源码并构建
COPY . .
RUN npm run build

# 生产环境部署阶段
FROM nginx:alpine

# 将构建产物复制到 nginx 默认静态文件目录
COPY --from=build /app/dist /usr/share/nginx/html

# 配置 Nginx：支持 Vue Router history 模式，并代理 API 请求到后端
RUN echo 'server { \
    listen       80; \
    server_name  localhost; \
    \
    location / { \
        root   /usr/share/nginx/html; \
        index  index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
    \
    location /api/ { \
        proxy_pass http://java-backend:8080/api/; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_connect_timeout 30s; \
        proxy_send_timeout 30s; \
        proxy_read_timeout 30s; \
    } \
}' > /etc/nginx/conf.d/default.conf

# 暴露 80 端口
EXPOSE 80

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
