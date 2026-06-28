# MyBlog

一个基于 Django + React 的简约博客系统，集成 Redis 缓存、Celery 异步任务、JWT 认证。

## 技术栈

**后端：** Django 6 / DRF / SimpleJWT / Celery / django-redis
**前端：** React 19 / Vite 8 / react-router-dom 7
**中间件：** Redis（缓存 + 消息代理）
**数据库：** SQLite（开发）/ PostgreSQL（生产）

## 快速开始（开发环境）

### 后端

```bash
cd myblog
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Linux/Mac

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

### Redis + Celery

```bash
# 启动 Redis（Windows 用 redis-server.exe）
redis-server

# 启动 Celery Worker
celery -A myblog worker --loglevel=info -P solo
```

访问：http://127.0.0.1:5173/

## 部署（生产环境）

### 前置条件
- Linux 服务器（Ubuntu 推荐）
- Nginx、Redis、PostgreSQL（可选）

### 一键部署

```bash
# 上传项目到服务器后
bash deploy.sh
```

### 手动配置

1. **设置环境变量（推荐用 systemd 或 .env）**

```bash
export DJANGO_DEBUG=False
export DJANGO_SECRET_KEY="生产环境随机密钥"
export DJANGO_ALLOWED_HOSTS="你的域名或IP"
export CORS_ALLOWED_ORIGINS="https://你的域名"
export CSRF_TRUSTED_ORIGINS="https://你的域名"
export USE_POSTGRES=True  # 可选
```

2. **构建前端**

```bash
cd frontend && npm run build
```

3. **收集静态文件**

```bash
python manage.py collectstatic --noinput
```

4. **启动服务**

```bash
# Gunicorn（4 worker）
gunicorn myblog.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --daemon

# Celery
celery -A myblog worker --loglevel=info -P solo --detach
```

5. **配置 Nginx**

见 `deploy.sh` 中的 Nginx 配置，或参考 [项目 Wiki](#)。

## API 接口

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | /api/posts/ | 文章列表（Redis 缓存） | - |
| GET | /api/posts/:id/ | 文章详情 | - |
| POST | /api/posts/:id/comments/ | 发表评论 | JWT |
| DELETE | /api/comments/:id/ | 删除评论 | JWT + 权限 |
| POST | /api/login/ | 登录（返回 JWT） | - |
| POST | /api/register/ | 注册（返回 JWT） | - |
| GET | /api/me/ | 当前用户信息 | JWT |
| POST | /api/token/refresh/ | 刷新 JWT | - |

## 项目结构

```
myblog/
├── blog/                    # Django 应用
│   ├── api.py               # DRF API 视图
│   ├── tasks.py             # Celery 异步任务
│   ├── models.py            # 数据模型
│   └── serializers.py       # 序列化器
├── frontend/                # React 前端
│   └── src/
│       ├── api.js           # API 封装（JWT 自动注入）
│       └── pages/           # 页面组件
├── myblog/                  # Django 项目配置
│   ├── settings.py          # 配置（支持环境变量）
│   └── celery.py            # Celery 实例
├── requirements.txt         # Python 依赖
├── deploy.sh                # 部署脚本
└── manage.py
```

## 环境变量参考

| 变量 | 默认值 | 说明 |
|------|--------|------|
| DJANGO_DEBUG | True | 调试模式 |
| DJANGO_SECRET_KEY | （开发用） | 生产环境务必更换 |
| DJANGO_ALLOWED_HOSTS | 127.0.0.1,localhost | 允许访问的域名 |
| USE_POSTGRES | False | 是否使用 PostgreSQL |
| DB_NAME / DB_USER / DB_PASSWORD | - | PostgreSQL 连接信息 |
| REDIS_URL | redis://127.0.0.1:6379/0 | Redis 缓存地址 |
| CELERY_BROKER_URL | redis://127.0.0.1:6379/1 | Celery 消息代理地址 |

## 许可证

MIT
