import os
from pydantic import BaseModel, HttpUrl, field_validator
from typing import List, Optional
from datetime import datetime
from enum import Enum
from app.core.config import settings

# --- Enums ---
class CompanyTypeEnum(str, Enum):
    MANUFACTURER = "manufacturer"
    INTEGRATOR = "integrator"
    DISTRIBUTOR = "distributor"
    SERVICE_PROVIDER = "service_provider"
    OTHER = "other"


class LanguageEnum(str, Enum):
    EN = "en"
    DE_CH = "de-CH"
    FR_CH = "fr-CH"
    IT_CH = "it-CH"


# --- CompanyTranslation Schemas ---
class CompanyTranslationBase(BaseModel):
    language: LanguageEnum
    name: str
    description: Optional[str] = None
    website: Optional[HttpUrl] = None
    logo: Optional[str] = None
    banner: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None


class CompanyTranslationCreate(CompanyTranslationBase):
    pass


class CompanyTranslationUpdate(BaseModel):
    language: Optional[LanguageEnum] = None
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[HttpUrl] = None
    logo: Optional[str] = None
    banner: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None


class CompanyTranslationResponse(BaseModel):
    id: str
    company_slug: str
    language: str
    name: str
    description: Optional[str] = None
    website: Optional[HttpUrl] = None
    logo: Optional[str] = None
    banner: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

    @field_validator("logo", "banner", mode="before")
    def prepend_base_url(cls, v):
        if v and not v.startswith("http"):
            return f"{settings.BASE_URL}/{v.lstrip('/')}"
        return v

    class Config:
        from_attributes = True


# --- Company Schemas ---
class CompanyBase(BaseModel):
    defult_name: str
    type: CompanyTypeEnum
    is_active: Optional[bool] = True


class CompanyCreate(CompanyBase):
    translations: List[CompanyTranslationCreate]


class CompanyUpdate(BaseModel):
    defult_name: Optional[str] = None
    type: Optional[CompanyTypeEnum] = None
    is_active: Optional[bool] = None
    translations: Optional[List[CompanyTranslationUpdate]] = None


class CompanyResponse(CompanyBase):
    slug: str
    created_at: datetime
    updated_at: datetime
    translations: List[CompanyTranslationResponse] = []

    class Config:
        from_attributes = True


# --- Pagination ---
class PaginatedCompanyResponse(BaseModel):
    total: int
    page: int
    size: int
    pages: int
    items: List[CompanyResponse]
