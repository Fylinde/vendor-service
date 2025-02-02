from sqlalchemy.orm import Session
from app.models.seller import SellerModel
from app.schemas.seller_schemas import SellerCreate
from datetime import datetime, timedelta

def get_seller(db: Session, seller_id: str):
    return db.query(SellerModel).filter(SellerModel.id == seller_id).first()

def create_seller(db: Session, seller_data: SellerCreate, is_verified: bool = False, is_approved: bool = False):
    """
    Creates a seller instance, handling hashed passwords and default values.
    
    Parameters:
    - db (Session): Database session instance.
    - seller_data (SellerCreate): Seller creation schema containing necessary seller details.
    - is_verified (bool): Determines if the seller is initially verified.
    - is_approved (bool): Determines if the seller is initially approved.
    
    Returns:
    - SellerModel: The newly created seller instance.
    """
    db_seller = SellerModel(
        full_name=seller_data.full_name,
        email=seller_data.email,
        phoneNumber=seller_data.phoneNumber,
        seller_type=seller_data.seller_type or "individual",
        currency_code=seller_data.currency_code,
        hashed_password=seller_data.password,  # Ensure password is hashed before calling this function
        is_email_verified=is_verified,
        is_phone_verified=is_verified,
        is_approved=is_approved,
    )

    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller






def get_seller_by_email(db: Session, email: str):
    return db.query(SellerModel).filter(SellerModel.email == email).first()

def get_seller_by_phone(db: Session, phoneNumber: str):
    """Retrieve a seller by phone number."""
    return db.query(SellerModel).filter(SellerModel.phoneNumber == phoneNumber).first()

def get_current_step(db: Session, seller_id: int):
    """Fetch the current registration step for a seller."""
    seller = db.query(SellerModel).filter(SellerModel.id == seller_id).first()
    if seller:
        return seller.current_step
    return None

def update_current_step(db: Session, seller_id: int, step: str, registration_data: dict = None):
    """Update the current registration step for a seller."""
    seller = db.query(SellerModel).filter(SellerModel.id == seller_id).first()
    if seller:
        seller.current_step = step
        if registration_data:
            seller.registration_data = registration_data
        db.commit()
        db.refresh(seller)
        return seller
    return None

def update_last_activity(seller_id: int, db: Session):
    seller = db.query(SellerModel).filter(SellerModel.id == seller_id).first()
    if seller:
        seller.lastActivityTimestamp = datetime.utcnow()
        db.commit()

def deactivate_inactive_sellers(db: Session, threshold_minutes: int = 30):
    threshold_time = datetime.utcnow() - timedelta(minutes=threshold_minutes)
    inactive_sellers = (
        db.query(SellerModel)
        .filter(SellerModel.lastActivityTimestamp < threshold_time, SellerModel.is_active == True)
        .all()
    )
    for seller in inactive_sellers:
        seller.is_active = False
    db.commit()