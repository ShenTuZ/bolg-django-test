# MyBlog

一个基于 Django + React 的简约博客系统，用于学习 Django 框架的核心功能。

## 技术栈

**后端**
- Django 6.0 — Python Web 框架
- Django REST Framework — API 构建
- django-simpleui — 后台管理界面美化
- SQLite — 数据库

**前端**
- React 19 — UI 框架
- Vite 8 — 构建工具
- react-router-dom 7 — 前端路由

## 功能

- 文章发布与管理（Django Admin）
- 文章分类
- 用户注册与登录（Session 认证）
- 文章评论（需登录）
- 评论删除（需权限）
- CSRF 保护
- 简约风格前端界面

## 快速开始

### 1. 克隆项目

```bash
git clone <repo-url>
cd myblog
```

### 2. 后端

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install django djangorestframework django-cors-headers django-simpleui

# 迁移数据库
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动服务
python manage.py runserver 0.0.0.0:8000
```

后台访问：http://127.0.0.1:8000/admin/

### 3. 前端

```bash
cd frontend
npm install
npm run dev
```

前端访问：http://127.0.0.1:5173/

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/csrf/ | 获取 CSRF Token |
| GET | /api/posts/ | 文章列表 |
| GET | /api/posts/:id/ | 文章详情（含评论） |
| POST | /api/posts/:id/comments/ | 发表评论（需登录） |
| DELETE | /api/comments/:id/delete/ | 删除评论（需权限） |
| POST | /api/login/ | 用户登录 |
| POST | /api/register/ | 用户注册 |
| POST | /api/logout/ | 退出登录 |
| GET | /api/me/ | 获取当前用户信息 |

## 项目结构

```
myblog/
├── blog/                    # Django 应用
│   ├── models.py            # 数据模型（Post, Comment, Category）
│   ├── api.py               # DRF API 视图
│   ├── serializers.py       # 序列化器
│   ├── admin.py             # 后台管理注册
│   └── views.py             # 模板视图
├── frontend/                # React 前端
│   └── src/
│       ├── api.js           # API 请求封装
│       ├── App.jsx          # 路由 & 导航
│       └── pages/           # 页面组件
├── myblog/                  # Django 项目配置
└── manage.py                # 管理脚本
```

## 许可证

MIT
