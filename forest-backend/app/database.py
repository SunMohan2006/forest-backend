"""
数据库连接管理 — 创建 SQLAlchemy 引擎、会话工厂、依赖注入函数
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# 数据库引擎（echo=True 可在开发时打印 SQL）
engine = create_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 基类 — 所有 model 继承此类
Base = declarative_base()


def get_db():
    """FastAPI 依赖注入：每个请求获取一个数据库会话，请求结束后自动关闭"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
