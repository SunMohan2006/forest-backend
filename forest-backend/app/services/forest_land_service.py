"""
林地业务逻辑 — 增删改查、搜索（含权限校验）
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.forest_land import ForestLand
from app.models.forest_image import ForestImage
from app.models.operation_log import OperationLog


def _check_permission(land: ForestLand, user_id: int, role: str, action: str) -> None:
    """权限校验：管理员可操作所有，普通用户只能操作自己创建的"""
    if role == "ADMIN":
        return
    if land.created_by != user_id:
        raise PermissionError(f"无权{action}：该林地由其他用户创建，只有创建者或管理员可以{action}")


def create(db: Session, data: dict, user_id: int) -> ForestLand:
    """新增林地，并记录操作日志"""
    land = ForestLand(**data, created_by=user_id)
    db.add(land)
    db.commit()
    db.refresh(land)

    log = OperationLog(
        user_id=user_id, action="CREATE", target="forest_land",
        target_id=land.id, detail=f"新增林地: {land.name}"
    )
    db.add(log)
    db.commit()

    return land


def update(db: Session, land_id: int, data: dict, user_id: int, role: str) -> ForestLand:
    """修改林地信息（需权限：创建者或管理员）"""
    land = db.query(ForestLand).filter(ForestLand.id == land_id).first()
    if not land:
        raise ValueError("林地不存在")
    _check_permission(land, user_id, role, "修改")

    for key, value in data.items():
        if value is not None:
            setattr(land, key, value)

    # SQLite 不支持 ON UPDATE CURRENT_TIMESTAMP，需手动设置
    land.updated_at = func.now()

    db.commit()
    db.refresh(land)

    log = OperationLog(
        user_id=user_id, action="UPDATE", target="forest_land",
        target_id=land.id, detail=f"修改林地: {land.name}"
    )
    db.add(log)
    db.commit()

    return land


def delete(db: Session, land_id: int, user_id: int, role: str) -> None:
    """删除林地（需权限：创建者或管理员，级联删除关联图片）"""
    land = db.query(ForestLand).filter(ForestLand.id == land_id).first()
    if not land:
        raise ValueError("林地不存在")
    _check_permission(land, user_id, role, "删除")

    db.delete(land)

    log = OperationLog(
        user_id=user_id, action="DELETE", target="forest_land",
        target_id=land_id, detail=f"删除林地: {land.name}"
    )
    db.add(log)
    db.commit()


def get_by_id(db: Session, land_id: int) -> Optional[ForestLand]:
    """查询单个林地详情（含关联图片数量）"""
    return db.query(ForestLand).filter(ForestLand.id == land_id).first()


def page_query(db: Session, page: int = 1, page_size: int = 10,
               keyword: str = None, land_type: str = None) -> dict:
    """分页查询林地列表，支持按名称模糊搜、按类型筛选"""
    query = db.query(ForestLand)

    # 模糊搜索（按名称或位置）
    if keyword:
        query = query.filter(
            ForestLand.name.contains(keyword) | ForestLand.location.contains(keyword)
        )
    # 按类型筛选
    if land_type:
        query = query.filter(ForestLand.land_type == land_type)

    total = query.count()
    records = (
        query.order_by(ForestLand.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    # 批量查询图片数量（修复 N+1 问题：原来每条记录一次 COUNT，现改为一次查询搞定）
    land_ids = [land.id for land in records]
    image_counts = {}
    if land_ids:
        counts = (
            db.query(ForestImage.land_id, func.count(ForestImage.id))
            .filter(ForestImage.land_id.in_(land_ids))
            .group_by(ForestImage.land_id)
            .all()
        )
        image_counts = {land_id: cnt for land_id, cnt in counts}

    # 给每条记录附加图片数量
    result = []
    for land in records:
        land_dict = {
            "id": land.id, "name": land.name, "area": float(land.area) if land.area else None,
            "location": land.location, "land_type": land.land_type,
            "tree_species": land.tree_species, "planting_year": land.planting_year,
            "canopy_density": float(land.canopy_density) if land.canopy_density else None,
            "description": land.description, "status": land.status,
            "created_by": land.created_by, "created_at": land.created_at,
            "updated_at": land.updated_at,
            "image_count": image_counts.get(land.id, 0),
        }
        result.append(land_dict)

    return {"total": total, "page": page, "page_size": page_size, "records": result}
