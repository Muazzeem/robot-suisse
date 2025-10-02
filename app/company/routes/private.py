import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.company.models import Company, generate_unique_slug
from app.company.schemas import CompanyUpdate, CompanyResponse

UPLOAD_DIR = "uploads/logos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/companies", tags=["private-companies"])

@router.put("/{company_slug}", response_model=CompanyResponse)
def update_company(company_slug: str, company: CompanyUpdate, db: Session = Depends(get_db)):
    db_company = db.query(Company).get(company_slug)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")

    for key, value in company.model_dump(exclude_unset=True).items():
        setattr(db_company, key, value)

    # If name is updated, regenerate slug
    if "name" in company.model_dump(exclude_unset=True):
        db_company.slug = generate_unique_slug(db, db_company.name, Company, exclude_slug=company_slug)

    db.commit()
    db.refresh(db_company)
    return db_company


@router.put("/{company_slug}/upload-logo")
async def upload_logo(company_slug: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Check if company exists
    db_company = db.query(Company).get(company_slug)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    file_ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"company_{company_slug}{file_ext}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"message": "Logo uploaded successfully", "logo_url": file_path}


@router.delete("/{company_slug}", status_code=204)
def delete_company(company_slug: str, db: Session = Depends(get_db)):
    db_company = db.query(Company).get(company_slug)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")

    db.delete(db_company)
    db.commit()
    return None