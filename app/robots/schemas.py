from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal


# ==================== RobotImage Schemas ====================

class RobotImageBase(BaseModel):
    url: str = Field(..., max_length=500)
    alt_text: Optional[str] = Field(None, max_length=255)
    position: int = Field(default=0, ge=0)
    is_primary: bool = Field(default=False)


class RobotImageCreate(RobotImageBase):
    pass


class RobotImageUpdate(BaseModel):
    url: Optional[str] = Field(None, max_length=500)
    alt_text: Optional[str] = Field(None, max_length=255)
    position: Optional[int] = Field(None, ge=0)
    is_primary: Optional[bool] = None


class RobotImageResponse(RobotImageBase):
    id: int
    robot_slug: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==================== Robot Schemas ====================

class RobotBase(BaseModel):
    name: str = Field(..., max_length=255, min_length=1)
    company_slug: str = Field(..., max_length=255)
    sku: Optional[str] = Field(None, max_length=100)
    model_number: Optional[str] = Field(None, max_length=100)
    series: Optional[str] = Field(None, max_length=100)
    
    # Classification
    robot_type: Optional[str] = Field(None, max_length=50, description="e.g., industrial_arm, mobile, humanoid")
    category: Optional[str] = Field(None, max_length=100, description="e.g., welding, pick_and_place")
    subcategory: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = Field(default=None, description="e.g., ['ROS2', 'AMR', 'collaborative']")
    
    # Key specs
    payload_kg: Optional[Decimal] = Field(None, ge=0, decimal_places=3, description="Payload capacity in kg")
    reach_mm: Optional[int] = Field(None, ge=0, description="Reach in millimeters")
    battery_capacity_wh: Optional[int] = Field(None, ge=0, description="Battery capacity in watt-hours")
    
    # Commerce
    unit_price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    currency: Optional[str] = Field(default="USD", max_length=3, pattern="^[A-Z]{3}$")
    in_stock: bool = Field(default=True)
    stock_qty: Optional[int] = Field(None, ge=0)
    lead_time_days: Optional[int] = Field(None, ge=0)
    warranty_months: Optional[int] = Field(None, ge=0)
    
    # Ops
    is_active: bool = Field(default=True)
    published_at: Optional[datetime] = None


class RobotCreate(RobotBase):
    slug: Optional[str] = None


class RobotUpdate(BaseModel):
    """Schema for updating an existing robot - all fields optional"""
    name: Optional[str] = Field(None, max_length=255, min_length=1)
    company_slug: Optional[str] = Field(None, max_length=255)
    sku: Optional[str] = Field(None, max_length=100)
    model_number: Optional[str] = Field(None, max_length=100)
    series: Optional[str] = Field(None, max_length=100)
    
    # Classification
    robot_type: Optional[str] = Field(None, max_length=50)
    category: Optional[str] = Field(None, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None
    
    # Key specs
    payload_kg: Optional[Decimal] = Field(None, ge=0, decimal_places=3)
    reach_mm: Optional[int] = Field(None, ge=0)
    battery_capacity_wh: Optional[int] = Field(None, ge=0)
    
    # Commerce
    unit_price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    currency: Optional[str] = Field(None, max_length=3, pattern="^[A-Z]{3}$")
    in_stock: Optional[bool] = None
    stock_qty: Optional[int] = Field(None, ge=0)
    lead_time_days: Optional[int] = Field(None, ge=0)
    warranty_months: Optional[int] = Field(None, ge=0)
    
    # Ops
    is_active: Optional[bool] = None
    published_at: Optional[datetime] = None


class RobotResponse(RobotBase):
    """Schema for robot responses - includes all fields plus generated ones"""
    slug: str
    created_at: datetime
    updated_at: datetime
    images: List[RobotImageResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class RobotListResponse(BaseModel):
    """Simplified robot response for list views"""
    slug: str
    name: str
    company_slug: str
    robot_type: Optional[str] = None
    category: Optional[str] = None
    unit_price: Optional[Decimal] = None
    currency: Optional[str] = None
    in_stock: bool
    is_active: bool
    primary_image: Optional[str] = None  # URL of primary image
    
    model_config = ConfigDict(from_attributes=True)


class PaginatedRobotResponse(BaseModel):
    """Paginated list of robots"""
    total: int
    page: int
    size: int
    pages: int
    items: List[RobotListResponse]



class RobotCreateWithImages(RobotCreate):
    """Create a robot with images in one request"""
    images: Optional[List[RobotImageCreate]] = Field(default=[], description="List of images to create with the robot")
