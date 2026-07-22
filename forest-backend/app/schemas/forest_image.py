"""
遥感图片相关 — 响应体校验模型
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ForestImageResponse(BaseModel):
    """图片信息返回"""
    id: int
    land_id: int
    image_url: str
    original_name: Optional[str] = None
    file_size: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True
