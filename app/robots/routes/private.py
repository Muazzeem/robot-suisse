import uuid
from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from app.db.database import get_db
from sqlalchemy.orm import Session, joinedload

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

@router.get("/{slug}", response_model=RobotResponse)
def get_robot(slug: str, db: Session = Depends(get_db)):
    robot = (
        db.query(Robot)
        .options(
            joinedload(Robot.images),
            joinedload(Robot.company)
        )
        .filter(Robot.slug == slug)
        .first()
    )
    if not robot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Robot not found"
        )
    return robot

@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_robot(slug: str, db: Session = Depends(get_db)):
    robot = db.query(Robot).filter(Robot.slug == slug).first()
    if not robot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Robot not found"
        )
    db.delete(robot)
    db.commit()
    return None
