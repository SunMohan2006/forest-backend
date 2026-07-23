"""
操作日志路由 — 管理员查看操作记录
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.operation_log import OperationLog
from app.utils.response import success, error

router = APIRouter(prefix="/api/log", tags=["📋 操作日志"])


@router.get("/list", summary="操作日志列表（管理员）",
            description="""
**功能说明**：分页查看系统操作日志，按时间倒序排列。

**权限要求**：仅管理员可查看。

**参数说明**：
- `page`：页码（默认 1）
- `page_size`：每页条数（默认 20，最多 100）
""")
def list_logs(page: int = Query(1, ge=1, description="页码"),
              page_size: int = Query(20, ge=1, le=100, description="每页条数"),
              db: Session = Depends(get_db),
              current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "ADMIN":
        return error(code=403, message="无权操作：仅管理员可查看操作日志")

    total = db.query(OperationLog).count()
    records = (
        db.query(OperationLog)
        .order_by(OperationLog.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return success(data={
        "total": total,
        "page": page,
        "page_size": page_size,
        "records": [{
            "id": r.id, "user_id": r.user_id, "action": r.action,
            "target": r.target, "target_id": r.target_id,
            "detail": r.detail, "created_at": str(r.created_at),
        } for r in records],
    })
