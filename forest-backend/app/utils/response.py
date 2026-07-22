"""
统一 API 返回格式 — 所有接口返回的数据都套这个结构
"""
from typing import Any, Optional
from pydantic import BaseModel


class ApiResponse(BaseModel):
    """标准响应体"""
    code: int = 200           # 业务状态码，200 成功
    message: str = "success"  # 提示信息
    data: Any = None          # 返回数据


def success(data: Any = None, message: str = "success") -> dict:
    """成功返回"""
    return {"code": 200, "message": message, "data": data}


def error(code: int = 400, message: str = "error", data: Any = None) -> dict:
    """失败返回"""
    return {"code": code, "message": message, "data": data}
