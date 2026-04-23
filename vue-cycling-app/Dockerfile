# 构建阶段
FROM node:18-alpine AS build
WORKDIR /app

# 复制 package.json 和 package-lock.json (如果存在)
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制项目所有文件
COPY . .

# 构建前端应用
RUN npm run build

# 生产环境部署阶段
FROM nginx:alpine

# 将构建产物复制到 nginx 的默认静态文件目录
COPY --from=build /app/dist /usr/share/nginx/html

# 将自定义 Nginx 配置复制进去 (如果需要代理请求到后端)
# 因为默认 Nginx 无法处理 Vue Router 的 history 模式，我们需要配置 try_files
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
    } \
}' > /etc/nginx/conf.d/default.conf

# 暴露 80 端口
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
