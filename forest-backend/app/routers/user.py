"""
用户路由 — 注册、登录、管理员用户管理
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_user
from app.schemas.user import RegisterRequest, LoginRequest
from app.services import user_service
from app.utils.response import success, error

router = APIRouter(prefix="/api/user", tags=["👤 用户模块"])


@router.post("/register", summary="用户注册",
             description="""
**功能说明**：注册一个新账号，用户名全局唯一。

**注意事项**：
- 用户名长度 2~50 个字符
- 密码长度至少 6 位
- 密码使用 bcrypt 加密存储，不会明文保存
- 默认注册角色为"普通用户"
""")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = user_service.register(db, req.username, req.password)
        return success(data={
            "id": user.id,
            "username": user.username,
            "role": user.role,
        }, message="注册成功")
    except ValueError as e:
        return error(code=400, message=str(e))


@router.post("/login", summary="用户登录",
             description="""
**功能说明**：验证用户名密码，成功则返回 JWT 访问令牌。

**使用步骤**：
1. 传入注册时的用户名和密码
2. 从返回结果中复制 `token` 字段的值
3. 点击本页面右上角 **"🔐 认证"** 按钮
4. 在弹出的对话框中输入 `Bearer <粘贴token>`，点击确认
5. 之后所有需要登录的接口都会自动携带令牌

**令牌有效期**：24 小时，过期后需重新登录
""")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    try:
        result = user_service.login(db, req.username, req.password)
        return success(data=result, message="登录成功")
    except ValueError as e:
        return error(code=401, message=str(e))


@router.get("/list", summary="用户列表（管理员）",
            description="**权限要求**：管理员。返回所有注册用户的信息（不含密码）。")
def list_users(db: Session = Depends(get_db),
               current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "ADMIN":
        return error(code=403, message="无权操作：仅管理员可查看用户列表")
    users = user_service.list_users(db)
    return success(data=users)


@router.put("/{user_id}/role", summary="修改用户角色（管理员）",
            description="**权限要求**：管理员。将指定用户的角色改为 ADMIN 或 USER。")
def change_role(user_id: int, new_role: str,
                db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "ADMIN":
        return error(code=403, message="无权操作：仅管理员可修改用户角色")
    try:
        user = user_service.change_role(db, user_id, new_role)
        return success(data={"id": user.id, "username": user.username, "role": user.role},
                       message=f"已将 {user.username} 的角色改为 {user.role}")
    except ValueError as e:
        return error(code=400, message=str(e))
