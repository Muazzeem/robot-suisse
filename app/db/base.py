import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/robot_suisse"
)

# Engine
engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def import_models():
    """
    Import all models to register them with SQLAlchemy's metadata.
    Must be called before Base.metadata.create_all() or Alembic migrations.
    """
    from app.company.models import Company  # noqa: F401
    from app.robots.models import Robot, RobotImage  # noqa: F401


import_models()
