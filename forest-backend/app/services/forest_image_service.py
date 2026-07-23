"""
遥感图片业务逻辑 — 上传、查询、删除
"""
import os
import uuid
from typing import List
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models.forest_land import ForestLand
from app.models.forest_image import ForestImage
from app.models.operation_log import OperationLog
from app.config import settings


def upload(db: Session, land_id: int, file: UploadFile, user_id: int, role: str,
            latitude: float = None, longitude: float = None) -> ForestImage:
    """上传遥感图片到指定林地（需权限：林地创建者或管理员）"""
    land = db.query(ForestLand).filter(ForestLand.id == land_id).first()
    if not land:
        raise ValueError("林地不存在")

    if role != "ADMIN" and land.created_by != user_id:
        raise PermissionError("无权上传：该林地由其他用户创建，只有创建者或管理员可以上传图片")

    ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    unique_name = f"{uuid.uuid4().hex}{ext}"

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(settings.UPLOAD_DIR, unique_name)
    content = file.file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    image = ForestImage(
        land_id=land_id,
        image_url=f"/uploads/{unique_name}",
        original_name=file.filename,
        file_size=len(content),
        latitude=latitude,
        longitude=longitude,
    )
    db.add(image)
    db.commit()
    db.refresh(image)

    log = OperationLog(
        user_id=user_id, action="CREATE", target="forest_image",
        target_id=image.id, detail=f"上传图片: {file.filename} → 林地 {land.name}"
    )
    db.add(log)
    db.commit()

    return image


def get_by_land(db: Session, land_id: int) -> List[ForestImage]:
    """查询某个林地下所有遥感图片"""
    return db.query(ForestImage).filter(ForestImage.land_id == land_id).order_by(ForestImage.uploaded_at.desc()).all()


def delete(db: Session, image_id: int, user_id: int, role: str) -> ForestImage:
    """删除图片（需权限：所属林地创建者或管理员，同时删除本地文件）"""
    image = db.query(ForestImage).filter(ForestImage.id == image_id).first()
    if not image:
        raise ValueError("图片不存在")

    # 权限校验：通过图片所属林地的 created_by 来判断
    land = db.query(ForestLand).filter(ForestLand.id == image.land_id).first()
    if role != "ADMIN" and land and land.created_by != user_id:
        raise PermissionError("无权删除：该图片所属林地由其他用户创建")

    # 删除本地文件
    file_path = os.path.join(settings.UPLOAD_DIR, os.path.basename(image.image_url))
    if os.path.exists(file_path):
        os.remove(file_path)

    # 删除数据库记录
    db.delete(image)

    log = OperationLog(
        user_id=user_id, action="DELETE", target="forest_image",
        target_id=image.id, detail=f"删除图片: {image.original_name}"
    )
    db.add(log)
    db.commit()

    return image
