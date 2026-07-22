"""
遥感图片业务逻辑 — 上传、查询
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


def upload(db: Session, land_id: int, file: UploadFile, user_id: int) -> ForestImage:
    """上传遥感图片到指定林地"""
    # 校验林地存在
    land = db.query(ForestLand).filter(ForestLand.id == land_id).first()
    if not land:
        raise ValueError("林地不存在")

    # 生成唯一文件名，防止覆盖
    ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    unique_name = f"{uuid.uuid4().hex}{ext}"

    # 确保上传目录存在
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # 保存文件到本地
    file_path = os.path.join(settings.UPLOAD_DIR, unique_name)
    content = file.file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # 数据库记录
    image = ForestImage(
        land_id=land_id,
        image_url=f"/uploads/{unique_name}",  # 相对路径，前端可直接访问
        original_name=file.filename,
        file_size=len(content),
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
