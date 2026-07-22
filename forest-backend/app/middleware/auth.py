"""
JWT 鉴权依赖 — FastAPI 依赖注入，校验请求头中的 Bearer Token
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.jwt_util import decode_token

# HTTPBearer: 自动从请求头 Authorization: Bearer <token> 中提取令牌
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    解析 JWT 令牌，返回当前登录用户信息。
    令牌无效或过期时，自动返回 401。

    用法：在路由函数参数中加上 current_user: dict = Depends(get_current_user)
    """
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌无效或已过期，请重新登录",
        )

    return {
        "user_id": payload.get("user_id"),
        "username": payload.get("username"),
        "role": payload.get("role"),
    }
