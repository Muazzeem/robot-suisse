import re
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean
from sqlalchemy.orm import Session, relationship
from app.db.base import Base

def slugify(name: str) -> str:
    """Convert name into a base slug (without uniqueness check)."""
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    return slug.strip('-')

def generate_unique_slug(db: Session, name: str) -> str:
    """Generate a unique slug for a company name."""
    base_slug = slugify(name)
    slug = base_slug
    counter = 1

    from app.company.models import Company 
    while db.query(Company).filter(Company.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug

class Company(Base):
    __tablename__ = "companies"

    slug = Column(String(255), primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    website = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    industry = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    robots = relationship(
        "Robot",
        back_populates="company",
        cascade="all, delete-orphan"
    )

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

