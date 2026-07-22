"""
林地模型 — 对应 forest_land 表
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class ForestLand(Base):
    __tablename__ = "forest_land"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="林地ID")
    name = Column(String(100), nullable=False, comment="林地名称")
    area = Column(Numeric(10, 2), comment="面积（亩）")
    location = Column(String(255), comment="地理位置")
    land_type = Column(String(50), comment="类型: 用材林/防护林/经济林/薪炭林/特用林")
    tree_species = Column(String(100), comment="主要树种，如落叶松、杉木、杨树")
    planting_year = Column(Integer, comment="种植年份，如 2018")
    canopy_density = Column(Numeric(3, 2), comment="郁闭度 (0.00~1.00)，如 0.75 表示林冠覆盖度75%")
    description = Column(Text, comment="描述")
    status = Column(String(20), nullable=False, default="ACTIVE", comment="状态: ACTIVE/INACTIVE")
    created_by = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), comment="创建人用户ID")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, onupdate=func.now(), comment="更新时间")

    # 多对一：多个林地属于一个创建人
    creator = relationship("User", back_populates="forest_lands")
    # 一对多：一个林地有多张遥感图片
    images = relationship("ForestImage", back_populates="forest_land", cascade="all, delete-orphan")
