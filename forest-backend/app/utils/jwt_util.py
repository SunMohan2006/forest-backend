"""
JWT 工具 — 生成令牌、校验令牌、从令牌中提取用户信息
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from app.config import settings


def create_access_token(user_id: int, username: str, role: str) -> str:
    """根据用户信息生成 JWT 令牌"""
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """解析 JWT 令牌，返回 payload；校验失败返回 None"""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
