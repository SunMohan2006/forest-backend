"""
用户相关 — 请求体 / 响应体校验模型
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    """注册请求"""
    username: str = Field(..., min_length=2, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=100, description="密码")


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserResponse(BaseModel):
    """用户信息返回（不含密码）"""
    id: int
    username: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True  # 允许从 SQLAlchemy 模型转换


class LoginResponse(BaseModel):
    """登录成功返回"""
    token: str
    user: UserResponse
