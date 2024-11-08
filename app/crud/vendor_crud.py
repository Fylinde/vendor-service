from sqlalchemy.orm import Session
from app.models.vendor import VendorModel
from app.schemas.vendor_schemas import VendorCreate
from app.utils.hash_utils import hash_password

def get_vendor(db: Session, vendor_id: int):
    return db.query(VendorModel).filter(VendorModel.id == vendor_id).first()


def create_vendor(db: Session, vendor: VendorCreate):
    db_vendor = VendorModel(
        name=vendor.name,
        email=vendor.email,
        hashed_password=hash_password(vendor.password)
    )
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def get_vendor_by_email(db: Session, email: str):
    return db.query(VendorModel).filter(VendorModel.email == email).first()
