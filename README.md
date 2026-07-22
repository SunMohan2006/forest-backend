# 🌲 林业资源信息管理后台

> **独立个人暑期项目** | 2026.7 — 2026.8 | FastAPI + SQLAlchemy + JWT

---

## 🔗 快速导航

| 想看什么 | 链接 |
|----------|------|
| 📖 **项目完整文档** | [forest-backend/README.md](forest-backend/README.md) |
| 📋 **接口在线文档（Swagger 中文版）** | 本地启动后访问 `/docs` |
| 🎯 **前端管理页面** | 本地启动后访问 `/` |

---

## ⚡ 30 秒跑起来

```bash
cd forest-backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

打开 http://localhost:8000/ — 不需要装数据库，不需要改配置。

---

## 📦 项目概要

| 维度 | 内容 |
|------|------|
| 技术栈 | FastAPI + SQLAlchemy + SQLite + JWT |
| 接口数量 | 15 个 REST API |
| 数据库表 | 4 张（用户 / 林地 / 遥感图片 / 操作日志） |
| 权限控制 | 管理员 + 普通用户双角色 |
| 前端 | 单文件 SPA（登录 → 数据管理 → 图片上传） |
| 开发日志 | [15 条踩坑记录](forest-backend/README.md#-开发日志) |
