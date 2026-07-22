# 林业资源信息管理后台

> **独立个人项目** | 开发周期：2026.7 - 2026.8 | FastAPI + MySQL + SQLAlchemy

## 项目简介

一个林业资源信息管理后端系统，支持林地数据 CRUD、遥感图片上传、多维度数据统计。

## 技术栈

- **后端框架**: FastAPI (Python)
- **数据库**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT (python-jose)
- **密码加密**: bcrypt (passlib)
- **文件上传**: python-multipart
- **API 文档**: Swagger (FastAPI 自动生成)

## 快速开始

### 1. 环境要求

- Python 3.9+
- MySQL 8.0+

### 2. 安装依赖

```bash
cd forest-backend
pip install -r requirements.txt
```

### 3. 初始化数据库

```bash
# 登录 MySQL 执行建表脚本
mysql -u root -p < sql/init.sql
```

### 4. 配置环境变量（可选）

默认配置在 `app/config.py`，可通过环境变量覆盖：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| DB_HOST | localhost | MySQL 地址 |
| DB_PORT | 3306 | MySQL 端口 |
| DB_USER | root | 数据库用户名 |
| DB_PASSWORD | root | 数据库密码 |
| DB_NAME | forest_db | 数据库名 |
| SECRET_KEY | (内置默认) | JWT 签名密钥 |

### 5. 启动服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 访问

- **Swagger 接口文档**: http://localhost:8000/docs
- **项目首页**: http://localhost:8000/

## 项目结构

```
forest-backend/
├── app/
│   ├── main.py              ← 启动入口
│   ├── config.py            ← 配置
│   ├── database.py          ← 数据库连接
│   ├── models/              ← SQLAlchemy 数据模型
│   ├── schemas/             ← Pydantic 请求/响应校验
│   ├── routers/             ← 路由控制器
│   ├── services/            ← 业务逻辑层
│   ├── middleware/          ← JWT 鉴权中间件
│   └── utils/               ← 工具函数
├── sql/init.sql             ← 建表 SQL
├── uploads/                 ← 图片上传目录
└── requirements.txt         ← Python 依赖
```

## API 接口一览

| 模块 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 用户 | POST | /api/user/register | 注册 |
| 用户 | POST | /api/user/login | 登录 |
| 林地 | POST | /api/forest-land | 新增 |
| 林地 | DELETE | /api/forest-land/{id} | 删除 |
| 林地 | PUT | /api/forest-land/{id} | 修改 |
| 林地 | GET | /api/forest-land/{id} | 详情 |
| 林地 | GET | /api/forest-land/page | 分页查询 |
| 林地 | GET | /api/forest-land/search | 搜索 |
| 图片 | POST | /api/forest-image/upload | 上传 |
| 图片 | GET | /api/forest-image/land/{landId} | 列表 |
| 统计 | GET | /api/statistics/overview | 总览 |
| 统计 | GET | /api/statistics/by-type | 类型分布 |
| 统计 | GET | /api/statistics/monthly-trend | 月度趋势 |
