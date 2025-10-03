import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL (defaults to local Postgres if not set)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/robot_suisse"
)

# Engine
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def import_models():
    """
    Import all models to register them with SQLAlchemy's metadata.
    Must be called before Base.metadata.create_all() or Alembic migrations.
    """
    # Company + related models
    from app.company.models import (
        Company,
        CompanyTranslation,
        CompanySocial,
        CompanyLocation,
        CompanyIndustry,
        CompanyCertification,
    )  # noqa: F401

    # Robots
    from app.robots.models import Robot, RobotImage  # noqa: F401

    # Auth
    from app.auth.models import User  # noqa: F401


# Ensure models are imported so metadata is aware of them
import_models()
