from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.vendor_schemas import VendorCreate, VendorResponse
from app.database import get_db
from app.services.vendor_service import register_vendor
from app.crud.vendor_crud import get_vendor
router = APIRouter()



@router.post("/register_vendor", response_model=VendorResponse)
def register_vendor_endpoint(vendor_data: VendorCreate, db: Session = Depends(get_db)):
    try:
        return register_vendor(db, vendor_data)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{vendor_id}", response_model=VendorResponse)
def read_vendor(vendor_id: int, db: Session = Depends(get_db)):
    db_vendor = get_vendor(db, vendor_id=vendor_id)
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor
