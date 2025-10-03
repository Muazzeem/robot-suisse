from math import ceil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.company.models import Company, CompanyTranslation
from app.company.schemas import (
    CompanyResponse,
    PaginatedCompanyResponse,
)

router = APIRouter(prefix="/companies", tags=["public-companies"])


# ------------------------
# List Companies (paginated)
# ------------------------
@router.get("/", response_model=PaginatedCompanyResponse)
def list_active_companies(
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Company).filter(Company.is_active == True)
    total = query.count()
    items = (
        query.offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "size": size,
        "pages": ceil(total / size) if total else 0,
        "items": items,
    }


# ------------------------
# Get Company by slug
# ------------------------
@router.get("/{company_slug}", response_model=CompanyResponse)
def get_company_by_slug(company_slug: str, db: Session = Depends(get_db)):
    company = db.query(Company).get(company_slug)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

