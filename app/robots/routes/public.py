from math import ceil
from fastapi import APIRouter, Depends, Query
from app.db.database import get_db
from sqlalchemy.orm import Session

from app.robots.models import Robot
from app.robots.schemas import PaginatedRobotResponse

router = APIRouter(prefix="/robots", tags=["public-robots"])

@router.get("/", response_model=PaginatedRobotResponse)
def list_robots(
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100),
    db: Session = Depends(get_db),
):
    total = db.query(Robot).count()
    items = (
        db.query(Robot)
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return {
        "total": total,
        "page": page,
        "size": size,
        "pages": ceil(total / size) if total > 0 else 0,
        "items": items,
    }
