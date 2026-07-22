"""
林地路由 — 增删改查、分页、搜索（需登录）
注意：固定路径 /page、/search 必须在动态路径 /{land_id} 前面，否则 FastAPI 会错误匹配
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.middleware.auth import get_current_user
from app.schemas.forest_land import ForestLandCreate, ForestLandUpdate
from app.services import forest_land_service
from app.utils.response import success, error

router = APIRouter(prefix="/api/forest-land", tags=["🌲 林地管理"])


@router.post("", summary="新增林地",
             description="""
**功能说明**：录入一条新的林地信息到系统中。

**字段说明**：
| 字段 | 必填 | 说明 |
|------|------|------|
| name | 是 | 林地名称，如"西山用材林" |
| area | 否 | 面积（亩），必须大于 0 |
| location | 否 | 地理位置，如"北京市西山" |
| land_type | 否 | 林地类型：用材林 / 防护林 / 经济林 / 薪炭林 / 特用林 |
| description | 否 | 补充描述，如主要树种、土壤类型等 |

**其他**：新增操作会自动记录到操作日志
""")
def create_land(req: ForestLandCreate, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    try:
        land = forest_land_service.create(db, req.model_dump(), current_user["user_id"])
        return success(data={
            "id": land.id, "name": land.name, "area": float(land.area) if land.area else None,
            "location": land.location, "land_type": land.land_type,
            "tree_species": land.tree_species, "planting_year": land.planting_year,
            "canopy_density": float(land.canopy_density) if land.canopy_density else None,
            "description": land.description, "status": land.status,
            "created_at": str(land.created_at),
        }, message="新增成功")
    except Exception as e:
        return error(code=500, message=str(e))


@router.get("/page", summary="分页查询林地列表",
            description="""
**功能说明**：分页获取林地列表，支持按关键词搜索和按类型筛选。

**参数说明**：
- `page`：页码，从 1 开始（默认 1）
- `page_size`：每页返回条数（默认 10，最多 100）
- `keyword`：模糊搜索关键词，同时匹配名称和位置
- `land_type`：按林地类型精确筛选

**示例**：`/api/forest-land/page?page=1&page_size=10&keyword=西山&land_type=用材林`
""")
def page_land(page: int = Query(1, ge=1, description="页码（从1开始）"),
              page_size: int = Query(10, ge=1, le=100, description="每页条数"),
              keyword: str = Query(None, description="按名称/位置模糊搜索"),
              land_type: str = Query(None, description="按类型筛选：用材林/防护林/经济林/薪炭林/特用林"),
              db: Session = Depends(get_db),
              current_user: dict = Depends(get_current_user)):
    result = forest_land_service.page_query(db, page, page_size, keyword, land_type)
    return success(data=result)


@router.get("/search", summary="搜索林地",
            description="""
**功能说明**：按关键词搜索林地，返回所有匹配结果（不分页）。

**示例**：`/api/forest-land/search?keyword=松树` 会找到所有名称或位置中包含"松树"的林地
""")
def search_land(keyword: str = Query(..., description="搜索关键词，同时匹配名称和位置"),
                db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    result = forest_land_service.page_query(db, page=1, page_size=999, keyword=keyword)
    return success(data=result["records"])


@router.get("/{land_id}", summary="查询林地详情",
            description="""
**功能说明**：根据林地 ID 获取单条林地的完整信息。

**示例**：`/api/forest-land/1` 返回 ID 为 1 的林地的全部字段
""")
def get_land(land_id: int, db: Session = Depends(get_db),
             current_user: dict = Depends(get_current_user)):
    land = forest_land_service.get_by_id(db, land_id)
    if not land:
        return error(code=404, message="林地不存在")
    return success(data={
        "id": land.id, "name": land.name, "area": float(land.area) if land.area else None,
        "location": land.location, "land_type": land.land_type,
        "tree_species": land.tree_species, "planting_year": land.planting_year,
        "canopy_density": float(land.canopy_density) if land.canopy_density else None,
        "description": land.description, "status": land.status,
        "created_by": land.created_by,
        "created_at": str(land.created_at),
        "updated_at": str(land.updated_at) if land.updated_at else None,
    })


@router.put("/{land_id}", summary="修改林地信息",
            description="""
**功能说明**：修改指定林地的一项或多项信息，只更新传入的字段，未传入的字段保持不变。

**示例**：只想改面积，只需传 `{"area": 200}` 即可，其他字段不会被清空
""")
def update_land(land_id: int, req: ForestLandUpdate, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    try:
        land = forest_land_service.update(db, land_id, req.model_dump(exclude_none=True), current_user["user_id"], current_user["role"])
        return success(data={
            "id": land.id, "name": land.name, "area": float(land.area) if land.area else None,
            "location": land.location, "land_type": land.land_type,
            "tree_species": land.tree_species, "planting_year": land.planting_year,
            "canopy_density": float(land.canopy_density) if land.canopy_density else None,
            "description": land.description, "status": land.status,
            "updated_at": str(land.updated_at) if land.updated_at else None,
        }, message="修改成功")
    except ValueError as e:
        return error(code=404, message=str(e))
    except PermissionError as e:
        return error(code=403, message=str(e))


@router.delete("/{land_id}", summary="删除林地",
              description="""
**功能说明**：删除指定林地，同时**级联删除**该林地下所有遥感图片（不可恢复，请谨慎操作）。
""")
def delete_land(land_id: int, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    try:
        forest_land_service.delete(db, land_id, current_user["user_id"], current_user["role"])
        return success(message="删除成功")
    except ValueError as e:
        return error(code=404, message=str(e))
    except PermissionError as e:
        return error(code=403, message=str(e))
