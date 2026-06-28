#!/bin/bash
# =============================================
# MyBlog 一键部署脚本（Ubuntu / CentOS）
# 用法：bash deploy.sh
# =============================================

set -e

echo "========================================"
echo "  MyBlog 部署脚本"
echo "========================================"

# ----- 1. 系统更新 + 安装依赖 -----
echo "[1/8] 安装系统依赖..."
if command -v apt &> /dev/null; then
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv nginx redis-server
elif command -v yum &> /dev/null; then
    sudo yum install -y python3 python3-pip nginx redis
fi

# ----- 2. 安装 Node.js（构建前端）-----
echo "[2/8] 安装 Node.js..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
    sudo apt install -y nodejs
fi

# ----- 3. 克隆项目（如果本地已经有代码就跳过）-----
# 实际部署时替换为你的仓库
# git clone https://github.com/ShenTuZ/bolg-django-test.git /home/www/myblog
# cd /home/www/myblog

# ----- 4. Python 虚拟环境 + 依赖 -----
echo "[3/8] 安装 Python 依赖..."
cd myblog
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# ----- 5. 数据库迁移 + 静态文件 -----
echo "[4/8] 数据库迁移..."
python manage.py migrate --run-syncdb

echo "[5/8] 收集静态文件..."
python manage.py collectstatic --noinput

# ----- 6. 构建前端 -----
echo "[6/8] 构建前端..."
cd frontend
npm install
npm run build
cd ..

# ----- 7. 配置 Nginx -----
echo "[7/8] 配置 Nginx..."
sudo tee /etc/nginx/sites-available/myblog > /dev/null << 'NGINX'
server {
    listen 80;
    server_name _;  # 改为你的域名或 IP

    # 前端静态文件
    root /home/www/myblog/frontend/dist;
    index index.html;

    # API 转发
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Admin 后台
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Django 静态文件
    location /static/ {
        alias /home/www/myblog/staticfiles/;
    }

    # 用户上传文件
    location /media/ {
        alias /home/www/myblog/media/;
    }

    # 前端路由（支持 React Router）
    location / {
        try_files $uri $uri/ /index.html;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/myblog /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# ----- 8. 启动 Gunicorn + Celery -----
echo "[8/8] 启动服务..."
pip install gunicorn

# 启动 Gunicorn（4 个 worker）
gunicorn myblog.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --daemon \
    --error-logfile /tmp/gunicorn.log

# 启动 Celery Worker
celery -A myblog worker --loglevel=info -P solo --detach

# 启动 Redis
sudo systemctl enable redis-server
sudo systemctl start redis-server

echo ""
echo "========================================"
echo "  部署完成！"
echo "  访问：http://服务器IP"
echo "  后台：http://服务器IP/admin/"
echo ""
echo "  创建管理员："
echo "  source venv/bin/activate && python manage.py createsuperuser"
echo "========================================"
