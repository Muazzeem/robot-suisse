import re
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session, relationship
from app.db.base import Base
from sqlalchemy import (
    Column, String, Text, Boolean, DateTime, ForeignKey, Enum
)
import enum

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

# Company Types
class CompanyType(enum.Enum):
    MANUFACTURER = "manufacturer"
    INTEGRATOR = "integrator"
    DISTRIBUTOR = "distributor"
    SERVICE_PROVIDER = "service_provider"
    OTHER = "other"


class Company(Base):
    __tablename__ = "companies"

    slug = Column(String(255), primary_key=True, index=True)
    type = Column(Enum(CompanyType), nullable=False, index=True)
    is_active = Column(Boolean, default=True)

    # General info
    website = Column(String(255), nullable=True)
    logo = Column(String(255), nullable=True)   # file path or URL
    banner = Column(String(255), nullable=True)

    # Relationships
    translations = relationship("CompanyTranslation", back_populates="company", cascade="all, delete-orphan")
    socials = relationship("CompanySocial", back_populates="company", cascade="all, delete-orphan")
    locations = relationship("CompanyLocation", back_populates="company", cascade="all, delete-orphan")
    industries = relationship("CompanyIndustry", back_populates="company", cascade="all, delete-orphan")
    certifications = relationship("CompanyCertification", back_populates="company", cascade="all, delete-orphan")

    # Keep robots!
    robots = relationship(
        "Robot",
        back_populates="company",
        cascade="all, delete-orphan"
    )

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Company slug={self.slug!r} type={self.type.value!r}>"


class LanguageEnum(enum.Enum):
    EN = "en"
    DE_CH = "de-CH"
    FR_CH = "fr-CH"
    IT_CH = "it-CH"

class CompanyTranslation(Base):
    __tablename__ = "company_translations"

    id = Column(String(36), primary_key=True)
    company_slug = Column(String(255), ForeignKey("companies.slug"), nullable=False)
    language = Column(Enum(LanguageEnum), nullable=False)  # dropdown automatically
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    company = relationship("Company", back_populates="translations")


class CompanySocial(Base):
    __tablename__ = "company_socials"

    id = Column(String(36), primary_key=True)
    company_slug = Column(String(255), ForeignKey("companies.slug"), nullable=False)
    platform = Column(String(50), nullable=False)  # e.g. linkedin, twitter, facebook
    url = Column(String(255), nullable=False)

    company = relationship("Company", back_populates="socials")


class CompanyLocation(Base):
    __tablename__ = "company_locations"

    id = Column(String(36), primary_key=True)
    company_slug = Column(String(255), ForeignKey("companies.slug"), nullable=False)
    language = Column(Enum(LanguageEnum), nullable=False)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)

    company = relationship("Company", back_populates="locations")


class CompanyIndustry(Base):
    __tablename__ = "company_industries"

    id = Column(String(36), primary_key=True)
    company_slug = Column(String(255), ForeignKey("companies.slug"), nullable=False)
    industry = Column(String(100), nullable=False)
    company = relationship("Company", back_populates="industries")


class CompanyCertification(Base):
    __tablename__ = "company_certifications"

    id = Column(String(36), primary_key=True)
    company_slug = Column(String(255), ForeignKey("companies.slug"), nullable=False)
    certification = Column(String(255), nullable=False)

    company = relationship("Company", back_populates="certifications")
