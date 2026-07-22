"""
用户业务逻辑 — 注册、登录
"""
import bcrypt
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.jwt_util import create_access_token


def _hash_password(password: str) -> str:
    """明文密码 → bcrypt 密文"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verify_password(password: str, hashed: str) -> bool:
    """校验明文密码与 bcrypt 密文是否匹配"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def register(db: Session, username: str, password: str) -> User:
    """用户注册。用户名已存在时抛出 ValueError"""
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise ValueError("用户名已被注册")

    user = User(
        username=username,
        password=_hash_password(password),
        role="USER",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login(db: Session, username: str, password: str) -> dict:
    """用户登录。校验用户名密码，返回 JWT 令牌和用户信息"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise ValueError("用户名或密码错误")

    if not _verify_password(password, user.password):
        raise ValueError("用户名或密码错误")

    token = create_access_token(user.id, user.username, user.role)

    return {
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "created_at": user.created_at,
        },
    }


def list_users(db: Session) -> list:
    """管理员：获取所有用户列表（不含密码）"""
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [{"id": u.id, "username": u.username, "role": u.role, "created_at": u.created_at} for u in users]


def change_role(db: Session, user_id: int, new_role: str) -> User:
    """管理员：修改用户角色"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("用户不存在")
    if new_role not in ("ADMIN", "USER"):
        raise ValueError("角色只能是 ADMIN 或 USER")
    user.role = new_role
    db.commit()
    db.refresh(user)
    return user
