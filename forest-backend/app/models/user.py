"""
用户模型 — 对应 user 表
"""
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码（bcrypt加密）")
    role = Column(String(20), nullable=False, default="USER", comment="角色: ADMIN / USER")
    created_at = Column(DateTime, server_default=func.now(), comment="注册时间")

    # 一对多：一个用户创建了多个林地
    forest_lands = relationship("ForestLand", back_populates="creator")
    # 一对多：一个用户有多条操作日志
    operation_logs = relationship("OperationLog", back_populates="user")
