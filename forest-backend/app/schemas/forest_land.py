"""
林地相关 — 请求体 / 响应体校验模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ForestLandCreate(BaseModel):
    """新增林地请求"""
    name: str = Field(..., min_length=1, max_length=100, description="林地名称")
    area: Optional[float] = Field(None, gt=0, description="面积（亩）")
    location: Optional[str] = Field(None, max_length=255, description="地理位置")
    land_type: Optional[str] = Field(None, max_length=50, description="类型: 用材林/防护林/经济林/薪炭林/特用林")
    tree_species: Optional[str] = Field(None, max_length=100, description="主要树种，如落叶松、杉木、杨树")
    planting_year: Optional[int] = Field(None, ge=1950, le=2099, description="种植年份")
    canopy_density: Optional[float] = Field(None, ge=0, le=1, description="郁闭度 (0~1)")
    description: Optional[str] = Field(None, description="描述")

    class Config:
        from_attributes = True


class ForestLandUpdate(BaseModel):
    """修改林地请求（所有字段可选，只更新传入的字段）"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="林地名称")
    area: Optional[float] = Field(None, gt=0, description="面积（亩）")
    location: Optional[str] = Field(None, max_length=255, description="地理位置")
    land_type: Optional[str] = Field(None, max_length=50, description="类型")
    tree_species: Optional[str] = Field(None, max_length=100, description="主要树种")
    planting_year: Optional[int] = Field(None, ge=1950, le=2099, description="种植年份")
    canopy_density: Optional[float] = Field(None, ge=0, le=1, description="郁闭度")
    description: Optional[str] = Field(None, description="描述")
    status: Optional[str] = Field(None, description="状态: ACTIVE/INACTIVE")


class ForestLandResponse(BaseModel):
    """林地详情返回"""
    id: int
    name: str
    area: Optional[float] = None
    location: Optional[str] = None
    land_type: Optional[str] = None
    tree_species: Optional[str] = None
    planting_year: Optional[int] = None
    canopy_density: Optional[float] = None
    description: Optional[str] = None
    status: str
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    image_count: Optional[int] = 0

    class Config:
        from_attributes = True


class ForestLandPageResponse(BaseModel):
    """林地分页查询返回"""
    total: int
    page: int
    page_size: int
    records: List[ForestLandResponse]
