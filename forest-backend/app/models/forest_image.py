"""
遥感图片模型 — 对应 forest_image 表
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class ForestImage(Base):
    __tablename__ = "forest_image"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="图片ID")
    land_id = Column(Integer, ForeignKey("forest_land.id", ondelete="CASCADE"), nullable=False, comment="所属林地ID")
    image_url = Column(String(500), nullable=False, comment="图片存储路径")
    original_name = Column(String(255), comment="原始文件名")
    file_size = Column(Integer, comment="文件大小（字节）")
    uploaded_at = Column(DateTime, server_default=func.now(), comment="上传时间")

    # 多对一：多张图片属于一个林地
    forest_land = relationship("ForestLand", back_populates="images")
