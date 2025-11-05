#!/bin/bash
echo "开始重建镜像..."

# 1. 停止并删除容器
docker-compose down

# 2. 查看当前项目的镜像
echo "当前镜像列表:"
docker-compose images

# 3. 重新构建（docker-compose build 会自动处理旧镜像）
docker-compose build --no-cache

# 4. 启动服务
docker-compose up -d

# 5. 验证
echo "重建完成，新镜像列表:"
docker-compose images
