import re
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import Column, String, Text, DateTime, Boolean
from sqlalchemy.orm import Session, relationship
from app.db.base import Base

def slugify(name: str) -> str:
    """Convert name into a base slug (without uniqueness check)."""
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    return slug.strip('-')

def generate_unique_slug(db: Session, name: str, model_class, exclude_slug: str = None) -> str:
    """
    Generate a unique slug for a given name and model class.
    Checks case-insensitively and supports excluding a current slug (for updates).
    """
    base_slug = slugify(name)
    slug = base_slug
    counter = 1

    while True:
        query = db.query(model_class).filter(func.lower(model_class.slug) == slug.lower())
        if exclude_slug:
            query = query.filter(model_class.slug != exclude_slug)

        exists = db.query(query.exists()).scalar()

        if not exists:
            return slug

        slug = f"{base_slug}-{counter}"
        counter += 1


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
    
    # Relationships - use string reference to avoid circular import
    robots = relationship(
        "Robot",
        back_populates="company",
        cascade="all, delete-orphan"
    )

    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Company slug={self.slug!r} name={self.name!r}>"
