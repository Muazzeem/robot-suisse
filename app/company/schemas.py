from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    email: EmailStr
    website: Optional[HttpUrl] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[HttpUrl] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class CompanyResponse(CompanyBase):
    slug: Optional[str]

    class Config:
        from_attributes = True


class PaginatedCompanyResponse(BaseModel):
    total: int
    page: int
    size: int
    pages: int
    items: List[CompanyResponse]