"""
FastAPI 应用入口 — 创建应用实例、注册路由、挂载静态文件
启动命令: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, FileResponse
import os

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

from app.database import engine, Base
from app.config import settings
from app.routers import user, forest_land, forest_image, statistics

# ── 创建应用（禁用默认 /docs，改用自定义路由注入中文汉化） ──
app = FastAPI(
    title="林业资源信息管理后台 API",
    description="""
## 📋 项目简介
独立个人暑期项目（2026 年 7-8 月），提供林地数据管理、遥感图片上传、数据统计分析等后端接口。

## 🔐 使用说明
1. **先注册账号** → `POST /api/user/register`
2. **登录获取令牌** → `POST /api/user/login`，拿到返回的 `token`
3. **点击页面右上角 "🔐 认证" 按钮** → 输入 `Bearer <你的token>`
4. **现在可以调用所有业务接口了**

## 🛠 技术栈
**FastAPI** + **SQLAlchemy** + **JWT 鉴权** + **文件上传**

## 📦 数据表
用户表 · 林地表 · 遥感图片表 · 操作日志表（共 4 张）
""",
    version="1.0.0",
    docs_url=None,    # 禁用默认文档页，改用下面自定义的中文版
    redoc_url=None,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # 默认折叠底部 Schema
        "displayRequestDuration": True,  # 显示请求耗时
        "filter": True,                  # 显示搜索框
        "tryItOutEnabled": True,         # 默认开启在线调试
    },
)

# ── 跨域配置 ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 挂载静态文件 ──
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ── 注册路由 ──
app.include_router(user.router)
app.include_router(forest_land.router)
app.include_router(forest_image.router)
app.include_router(statistics.router)

# ── 挂载上传文件目录 ──
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


# ── 自定义 Swagger 文档页（注入中文汉化脚本） ──
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    """返回注入了中文翻译脚本的 Swagger 页面"""
    html = get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=f"{app.title} - 接口文档",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_ui_parameters=app.swagger_ui_parameters,
    )
    # 在 </body> 前注入汉化 JS 脚本
    injected = html.body.decode("utf-8").replace(
        "</body>",
        '<script src="/static/swagger-zh.js"></script>\n</body>',
    )
    return HTMLResponse(content=injected)


@app.on_event("startup")
def on_startup():
    """启动时建表 + 初始化管理员账号"""
    import app.models  # noqa: F401
    Base.metadata.create_all(bind=engine)

    # 初始化管理员账号（不存在则创建）
    from app.database import SessionLocal
    from app.models.user import User
    import bcrypt
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin",
            password=bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode(),
            role="ADMIN",
        )
        db.add(admin)
        db.commit()
        print("[OK] 管理员账号已创建: admin / admin123")
    elif admin.role != "ADMIN":
        admin.role = "ADMIN"
        db.commit()
        print("[OK] 管理员权限已修复")
    db.close()


@app.get("/", summary="前端管理页面")
def root():
    """返回前端管理页面（登录 → 林地管理 → 图片查看）"""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))
