"""
操作日志模型 — 对应 operation_log 表
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class OperationLog(Base):
    __tablename__ = "operation_log"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="日志ID")
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), comment="操作人用户ID")
    action = Column(String(50), comment="操作类型: CREATE/UPDATE/DELETE")
    target = Column(String(100), comment="操作对象: forest_land/forest_image")
    target_id = Column(Integer, comment="操作对象ID")
    detail = Column(String(500), comment="操作详情")
    created_at = Column(DateTime, server_default=func.now(), comment="操作时间")

    # 多对一：多条日志属于一个用户
    user = relationship("User", back_populates="operation_logs")
