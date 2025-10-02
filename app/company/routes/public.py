from math import ceil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.company.models import Company, generate_unique_slug
from app.company.schemas import CompanyCreate, CompanyResponse, PaginatedCompanyResponse

router = APIRouter(prefix="/companies", tags=["public-companies"])

@router.post("/", response_model=CompanyResponse, status_code=201)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    data = company.model_dump()

    if data.get("website"):
        data["website"] = str(data["website"])

    data["slug"] = generate_unique_slug(db, data["name"])

    db_company = Company(**data)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@router.get("/", response_model=PaginatedCompanyResponse)
def list_companies(
    page: int = Query(1, ge=1),
    size: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    total = db.query(Company).count()
    items = (
        db.query(Company)
        .offset((page - 1) * size)
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

@router.get("/{company_slug}", response_model=CompanyResponse)
def get_company_by_slug(company_slug: str, db: Session = Depends(get_db)):
    company = db.query(Company).get(company_slug)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company