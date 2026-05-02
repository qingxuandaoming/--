#!/bin/bash
# 骑行装备数据分析系统 - Docker 一键构建脚本 (Linux/macOS)
set -e

echo "============================================================"
echo "  骑行装备数据分析系统 - Docker 一键构建脚本"
echo "============================================================"
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker 未安装或未在 PATH 中"
    exit 1
fi

# 检查 Compose
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
elif docker-compose --version &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    echo "[ERROR] docker-compose / docker compose 未找到"
    exit 1
fi

echo "[INFO] 使用命令: $COMPOSE_CMD"
echo ""

# 构建镜像
echo "[Step 1/3] 构建 Docker 镜像..."
$COMPOSE_CMD -p cycling_system build --no-cache
echo "  镜像构建成功"
echo ""

# 启动服务
echo "[Step 2/3] 启动服务..."
$COMPOSE_CMD -p cycling_system up -d
echo "  服务已启动"
echo ""

# 等待并显示状态
echo "[Step 3/3] 检查服务状态..."
sleep 5
$COMPOSE_CMD -p cycling_system ps
echo ""

# 显示访问信息
echo "============================================================"
echo "  Docker 部署完成！"
echo "============================================================"
echo ""
echo "  前端访问: http://localhost"
echo "  Java API: http://localhost:8080/api/route/health"
echo "  Python API: http://localhost:5000/api/health"
echo ""
echo "  常用命令:"
echo "    查看日志: $COMPOSE_CMD -p cycling_system logs -f"
echo "    停止服务: $COMPOSE_CMD -p cycling_system down"
echo "    重启服务: $COMPOSE_CMD -p cycling_system restart"
echo "============================================================"
