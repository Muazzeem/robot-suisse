from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Integer,
    Numeric,
    JSON,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class RobotImage(Base):
    __tablename__ = "robot_images"

    id = Column(Integer, primary_key=True, index=True)
    robot_slug = Column(String(255), ForeignKey("robots.slug", ondelete="CASCADE"), nullable=False, index=True)

    url = Column(String(500), nullable=False)
    alt_text = Column(String(255), nullable=True)
    position = Column(Integer, default=0, nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship back to Robot
    robot = relationship("Robot", back_populates="images")

    def __repr__(self) -> str:
        return f"<RobotImage id={self.id} robot_slug={self.robot_slug} url={self.url!r} primary={self.is_primary}>"


class Robot(Base):
    __tablename__ = "robots"

    slug = Column(String(255), primary_key=True, index=True)
    company_slug = Column(String(255), ForeignKey("companies.slug", ondelete="CASCADE"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False, index=True)
    sku = Column(String(100), nullable=True, unique=True, index=True)
    model_number = Column(String(100), nullable=True, index=True)
    series = Column(String(100), nullable=True)

    # Relationships
    images = relationship(
        "RobotImage",
        back_populates="robot",
        cascade="all, delete-orphan",
        order_by="RobotImage.position"
    )
    company = relationship("Company", back_populates="robots")

    # Classification
    robot_type = Column(String(50), nullable=True, index=True)
    category = Column(String(100), nullable=True, index=True)
    subcategory = Column(String(100), nullable=True, index=True)
    tags = Column(JSON, nullable=True)

    # Key specs
    payload_kg = Column(Numeric(10, 3), nullable=True)
    reach_mm = Column(Integer, nullable=True)
    battery_capacity_wh = Column(Integer, nullable=True)
    # Commerce
    unit_price = Column(Numeric(12, 2), nullable=True)
    currency = Column(String(3), nullable=True, default="USD")
    in_stock = Column(Boolean, default=True, nullable=False)
    stock_qty = Column(Integer, nullable=True)
    lead_time_days = Column(Integer, nullable=True)
    warranty_months = Column(Integer, nullable=True)

    # Ops
    is_active = Column(Boolean, default=True, nullable=False)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Robot slug={self.slug!r} name={self.name!r} company={self.company_slug!r} active={self.is_active}>"