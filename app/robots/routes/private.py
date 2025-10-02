import uuid
from fastapi import APIRouter, Depends, Query
from app.db.database import get_db
from sqlalchemy.orm import Session

from app.company.models import slugify, generate_unique_slug

from app.robots.models import Robot
from app.robots.schemas import RobotResponse, RobotCreate

router = APIRouter(prefix="/robots", tags=["public-robots"])

@router.post("/", response_model=RobotResponse)
def create_robot(robot_in: RobotCreate, db: Session = Depends(get_db)):
    slug = generate_unique_slug(db, robot_in.name, model_class=Robot)
    sku = slugify(robot_in.sku) if robot_in.sku else str(uuid.uuid4())
    db_robot = Robot(**robot_in.model_dump(exclude={"slug", "sku"}), slug=slug, sku=sku)
    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)
    return db_robot