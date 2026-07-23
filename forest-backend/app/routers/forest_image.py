"""
遥感图片路由 — 上传、查看列表、删除（需登录）
"""
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services import forest_image_service
from app.utils.response import success, error

router = APIRouter(prefix="/api/forest-image", tags=["🖼 图片管理"])


@router.post("/upload", summary="上传遥感图片",
             description="""
**功能说明**：上传一张遥感图片并绑定到指定林地。

**限制**：
- 支持格式：JPG / PNG / GIF / WebP / TIFF
- 文件大小上限：10MB
- 文件名会自动重命名为 UUID 防止冲突

**上传后**：图片可通过 `/uploads/<文件名>` 直接访问
""")
async def upload_image(land_id: int,
                       file: UploadFile = File(...),
                       latitude: float = Query(None, description="纬度"),
                       longitude: float = Query(None, description="经度"),
                       db: Session = Depends(get_db),
                       current_user: dict = Depends(get_current_user)):
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp", "image/tiff"]
    if file.content_type not in allowed_types:
        return error(code=400, message=f"不支持的文件类型: {file.content_type}，仅支持 JPG/PNG/GIF/WebP/TIFF")

    try:
        image = forest_image_service.upload(db, land_id, file, current_user["user_id"], current_user["role"],
                                             latitude=latitude, longitude=longitude)
        return success(data={
            "id": image.id, "land_id": image.land_id,
            "image_url": image.image_url, "original_name": image.original_name,
            "file_size": image.file_size, "latitude": float(image.latitude) if image.latitude else None,
            "longitude": float(image.longitude) if image.longitude else None,
            "uploaded_at": str(image.uploaded_at),
        }, message="上传成功")
    except ValueError as e:
        return error(code=404, message=str(e))
    except PermissionError as e:
        return error(code=403, message=str(e))


@router.get("/land/{land_id}", summary="查看某林地的所有图片",
            description="""
**功能说明**：返回指定林地下的所有遥感图片列表，按上传时间倒序排列。

**示例**：`/api/forest-image/land/1` 返回 ID 为 1 的林地下所有图片
""")
def list_images(land_id: int, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    images = forest_image_service.get_by_land(db, land_id)
    return success(data=[{
        "id": img.id, "land_id": img.land_id,
        "image_url": img.image_url, "original_name": img.original_name,
        "file_size": img.file_size,
        "latitude": float(img.latitude) if img.latitude else None,
        "longitude": float(img.longitude) if img.longitude else None,
        "uploaded_at": str(img.uploaded_at),
    } for img in images])


@router.delete("/{image_id}", summary="删除遥感图片",
               description="""
**功能说明**：删除一张遥感图片（需权限：图片所属林地的创建者或管理员）。

**注意**：同时删除本地文件和数据库记录，不可恢复。
""")
def delete_image(image_id: int, db: Session = Depends(get_db),
                 current_user: dict = Depends(get_current_user)):
    try:
        image = forest_image_service.delete(db, image_id, current_user["user_id"], current_user["role"])
        return success(data={"id": image.id, "original_name": image.original_name}, message="删除成功")
    except ValueError as e:
        return error(code=404, message=str(e))
    except PermissionError as e:
        return error(code=403, message=str(e))
