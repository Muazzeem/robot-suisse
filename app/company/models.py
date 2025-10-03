import re
import enum
from datetime import datetime
import uuid
from sqlalchemy import (
    Column, String, Text, Boolean, DateTime, Enum, JSON, event, ForeignKey
)
from sqlalchemy.orm import validates, relationship
from app.db.base import Base


# --- Helpers ---
def slugify(name: str) -> str:
    """Convert name into a slug (no uniqueness check)."""
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    return slug.strip('-')


# --- Enums ---
class CompanyType(enum.Enum):
    MANUFACTURER = "manufacturer"
    INTEGRATOR = "integrator"
    DISTRIBUTOR = "distributor"
    SERVICE_PROVIDER = "service_provider"
    OTHER = "other"


class LanguageEnum(enum.Enum):
    EN = "en"
    DE_CH = "de-CH"
    FR_CH = "fr-CH"
    IT_CH = "it-CH"


class CompanyType(enum.Enum):
    MANUFACTURER = "manufacturer"
    INTEGRATOR = "integrator"
    DISTRIBUTOR = "distributor"
    SERVICE_PROVIDER = "service_provider"
    OTHER = "other"


class LanguageEnum(enum.Enum):
    EN = "en"
    DE_CH = "de-CH"
    FR_CH = "fr-CH"
    IT_CH = "it-CH"


# --- Main Company ---
class Company(Base):
    __tablename__ = "companies"

    slug = Column(String(255), primary_key=True, index=True)
    defult_name = Column(String(255), nullable=False)
    type = Column(Enum(CompanyType), nullable=False, index=True)
    is_active = Column(Boolean, default=True)

    translations = relationship(
        "CompanyTranslation",
        back_populates="company",
        cascade="all, delete-orphan"
    )
    robots = relationship(
        "Robot",
        back_populates="company",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Company slug={self.slug!r} type={self.type.value!r}>"


class CompanyTranslation(Base):
    __tablename__ = "company_translations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_slug = Column(String(255), ForeignKey("companies.slug"), nullable=False)
    language = Column(Enum(LanguageEnum), nullable=False)

    # Translatable fields
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    logo = Column(String(255), nullable=True)
    banner = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    company = relationship("Company", back_populates="translations")


# --- Auto-generate slug on insert/update ---
@event.listens_for(Company, "before_insert")
def before_insert(mapper, connection, target):
    if not target.slug and target.defult_name:
        target.slug = slugify(target.defult_name)


@event.listens_for(Company, "before_update")
def before_update(mapper, connection, target):
    # Optional: regenerate slug if name changes
    if target.defult_name and not target.slug:
        target.slug = slugify(target.defult_name)
