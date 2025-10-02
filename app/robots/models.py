from datetime import datetime
from app.company.models import Company
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Integer,
    Numeric,
    JSON,
)
from app.db.base import Base


from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class RobotImage(Base):
    __tablename__ = "robot_images"

    id = Column(Integer, primary_key=True, index=True)
    obot_id = Column(Integer, ForeignKey("robots.id", ondelete="CASCADE"), nullable=False, index=True)

    url = Column(String(500), nullable=False)
    alt_text = Column(String(255), nullable=True)       # Accessibility / SEO
    position = Column(Integer, default=0, nullable=False)  # ordering for carousel
    is_primary = Column(Boolean, default=False, nullable=False)  # mark the main/default image

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship back to Robot
    robot = relationship("Robot", back_populates="images")

    def __repr__(self) -> str:
        return f"<RobotImage id={self.id} robot_id={self.robot_id} url={self.url!r} primary={self.is_primary}>"



class Robot(Base):
    __tablename__ = "robots"

    slug = Column(String(255), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    sku = Column(String(100), nullable=True, unique=True, index=True)
    model_number = Column(String(100), nullable=True, index=True)
    series = Column(String(100), nullable=True)                           # product line/series (not company)

    images = relationship(
        "RobotImage",
        back_populates="robot",
        cascade="all, delete-orphan",
        order_by="RobotImage.position"
    )
    company = relationship(
        "Company",
        back_populates="robots")
    # Classification
    robot_type = Column(String(50), nullable=True, index=True)            # e.g. "industrial_arm", "mobile", "humanoid", "service"
    category = Column(String(100), nullable=True, index=True)             # e.g. "welding", "pick_and_place"
    subcategory = Column(String(100), nullable=True, index=True)
    tags = Column(JSON, nullable=True)                                    # ["ROS2", "AMR", "collaborative"]

    # Key specs (keep names buyer-friendly)
    payload_kg = Column(Numeric(10, 3), nullable=True)
    reach_mm = Column(Integer, nullable=True)

    battery_capacity_wh = Column(Integer, nullable=True)
    runtime_hours = Column(Numeric(6, 2), nullable=True)
    sensors = Column(JSON, nullable=True)                                 # ["Lidar", "RGBD", "IMU"]
    interfaces = Column(JSON, nullable=True)                              # ["Ethernet", "CAN", "RS485", "Wi-Fi", "5G"]
    software = Column(JSON, nullable=True)                                # {"sdk": ["ROS2 Humble"], "apis": ["Python", "C++"]}
    applications = Column(JSON, nullable=True)                            # ["material_handling", "inspection"]
    compatible_end_effectors = Column(JSON, nullable=True)                # ["gripper", "welder"]
    accessories = Column(JSON, nullable=True)
    safety_standards = Column(JSON, nullable=True)                        # ["ISO 10218", "ISO/TS 15066"]
    certifications = Column(JSON, nullable=True)                          # ["CE", "FCC"]

    # Commerce
    unit_price = Column(Numeric(12, 2), nullable=True)
    currency = Column(String(3), nullable=True, default="USD")
    price_valid_from = Column(DateTime, nullable=True)
    price_valid_to = Column(DateTime, nullable=True)
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
        return f"<Robot id={self.id} name={self.name!r} slug={self.slug!r} active={self.is_active}>"
