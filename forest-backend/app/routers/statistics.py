"""
数据统计路由 — 总览、类型分布、月度趋势（需登录）
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.forest_land import ForestLand
from app.models.forest_image import ForestImage
from app.utils.response import success

router = APIRouter(prefix="/api/statistics", tags=["📊 数据统计"])


@router.get("/overview", summary="数据总览",
            description="""
**功能说明**：返回系统核心指标一览。

**返回内容**：
- 林地总数
- 活跃林地数量（状态为 ACTIVE）
- 遥感图片总数
""")
def overview(db: Session = Depends(get_db),
             current_user: dict = Depends(get_current_user)):
    land_count = db.query(ForestLand).count()
    image_count = db.query(ForestImage).count()
    active_count = db.query(ForestLand).filter(ForestLand.status == "ACTIVE").count()

    return success(data={
        "total_lands": land_count,
        "active_lands": active_count,
        "total_images": image_count,
    })


@router.get("/by-type", summary="按林地类型分布",
            description="""
**功能说明**：统计每种林地类型（用材林/防护林/经济林/薪炭林/特用林）各有多少条记录。

**用途**：可用于绘制饼图，直观展示林业资源类型结构
""")
def by_type(db: Session = Depends(get_db),
            current_user: dict = Depends(get_current_user)):
    results = (
        db.query(ForestLand.land_type, func.count(ForestLand.id).label("count"))
        .group_by(ForestLand.land_type)
        .all()
    )
    return success(data=[{"land_type": r[0] or "未分类", "count": r[1]} for r in results])


@router.get("/monthly-trend", summary="近30天新增趋势",
            description="""
**功能说明**：按天统计最近 30 天新增林地的数量变化趋势。

**用途**：可用于绘制折线图，观察数据录入活跃度变化
""")
def monthly_trend(db: Session = Depends(get_db),
                  current_user: dict = Depends(get_current_user)):
    thirty_days_ago = datetime.now() - timedelta(days=30)

    results = (
        db.query(func.date(ForestLand.created_at).label("date"), func.count(ForestLand.id).label("count"))
        .filter(ForestLand.created_at >= thirty_days_ago)
        .group_by(func.date(ForestLand.created_at))
        .order_by("date")
        .all()
    )
    return success(data=[{"date": str(r[0]), "count": r[1]} for r in results])


@router.get("/by-species", summary="按树种分布统计",
            description="""
**功能说明**：统计每种树种的林地数量和总面积。

**用途**：了解林业资源中不同树种的种植规模，辅助树种结构优化决策。

**林业背景**：不同树种经营周期和用途差异大——落叶松生长快适合作建筑材，杉木适合作家具材。
""")
def by_species(db: Session = Depends(get_db),
               current_user: dict = Depends(get_current_user)):
    results = (
        db.query(
            ForestLand.tree_species,
            func.count(ForestLand.id).label("count"),
            func.sum(ForestLand.area).label("total_area")
        )
        .group_by(ForestLand.tree_species)
        .all()
    )
    return success(data=[{
        "tree_species": r[0] or "未指定",
        "count": r[1],
        "total_area": float(r[2]) if r[2] else 0,
    } for r in results])


@router.get("/by-planting-year", summary="按种植年份统计",
            description="""
**功能说明**：按种植年份分组统计林地数量，直观展示各年份造林规模。

**用途**：识别不同年份的造林高峰期，辅助判断各批次林地的生长阶段和抚育需求。
""")
def by_planting_year(db: Session = Depends(get_db),
                     current_user: dict = Depends(get_current_user)):
    results = (
        db.query(ForestLand.planting_year, func.count(ForestLand.id).label("count"))
        .filter(ForestLand.planting_year.isnot(None))
        .group_by(ForestLand.planting_year)
        .order_by(ForestLand.planting_year)
        .all()
    )
    return success(data=[{"planting_year": r[0], "count": r[1]} for r in results])
