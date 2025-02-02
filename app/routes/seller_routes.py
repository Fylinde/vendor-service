from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.seller_schemas import SellerCreate, SellerResponse
from app.database import get_db
from app.models.seller import SellerModel
from app.services.seller_service import register_seller
from app.crud.seller_crud import get_seller, get_seller_by_email
import logging
from app.schemas.seller_schemas import SellerVerificationUpdateRequest, ResendVerificationCodeRequest
from app.services.seller_service import get_seller_details, update_seller_details, get_seller_current_step, update_seller_step
from app.schemas.seller_schemas import SellerBase, CurrentStepRequest, CurrentStepResponse, EmailRequest
from app.utils.email_service import send_email  # Assuming send_email is in email_service.py
from app.services.seller_service import record_seller_activity
from app.services.seller_service import handle_resend_verification_code
router = APIRouter()

@router.post("/register_seller", response_model=SellerResponse)
def register_seller_endpoint(seller_data: SellerCreate, db: Session = Depends(get_db)):
    logging.info(f"Received seller registration data: {seller_data.dict()}")
    try:
        return register_seller(db, seller_data)
    except HTTPException as e:
        logging.error(f"HTTPException: {e.detail}")
        raise


@router.get("/{seller_id}", response_model=SellerResponse)
def read_seller(seller_id: int, db: Session = Depends(get_db)):
    db_seller = get_seller(db, seller_id=seller_id)
    if db_seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return db_seller


@router.post("/mark_verified", summary="Mark seller as verified")
def mark_seller_as_verified(
    email: str, 
    is_email: bool = True,  # Default to email verification
    db: Session = Depends(get_db)
):
    seller = get_seller_by_email(db, email)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    
    # Update the seller's verified status based on the verification method
    if is_email:
        seller.is_email_verified = True
    else:
        seller.is_phone_verified = True
    
    db.commit()
    return {"status": "Seller marked as verified by email" if is_email else "Seller marked as verified by phone"}


# @router.post("/update_verification_status", summary="Update seller's verification status")
# async def update_seller_status(
#     payload: SellerVerificationUpdateRequest,  # Use schema for payload validation
#     db: Session = Depends(get_db)
# ):
#     sellerId = payload.sellerId
#     is_email = payload.is_email

#     # Log the received payload to verify format
#     logging.info(f"Received update request for seller_id: {sellerId}, is_email: {is_email}")

#     # Fetch seller by ID
#     seller = db.query(SellerModel).filter(SellerModel.id == sellerId).first()
#     if not seller:
#         raise HTTPException(status_code=404, detail="Seller not found")

#     # Update the seller's verified status based on the verification method
#     if is_email:
#         seller.is_email_verified = True
#     else:
#         seller.is_phone_verified = True
    
#     db.commit()
#     return {"status": "Seller verified by email" if is_email else "Seller verified by phone"}


@router.post("/update_verification_status", summary="Update seller's verification status")
async def update_seller_status(
    payload: SellerVerificationUpdateRequest,  # Use schema for payload validation
    db: Session = Depends(get_db)
):
    """
    Receives verification status update from auth-service and updates the seller's verification status
    in the vendor-service database.
    
    Parameters:
    - payload (SellerVerificationUpdateRequest): Contains sellerId, is_email flag, and verification method.
    - db (Session): Database session instance.
    
    Returns:
    - dict: Success or failure message.
    """
    try:
        logging.info(f"Received verification update for seller ID: {payload.sellerId}")
        
        # Fetch the seller record from the database
        seller = db.query(SellerModel).filter(SellerModel.id == payload.sellerId).first()
        
        if not seller:
            logging.warning(f"Seller ID {payload.sellerId} not found.")
            raise HTTPException(status_code=404, detail="Seller not found.")
        
        # Update seller's verification status based on the verification method
        if payload.is_email:
            seller.is_email_verified = True
            logging.info(f"Seller ID {payload.sellerId} email verified successfully.")
        else:
            seller.is_phone_verified = True
            logging.info(f"Seller ID {payload.sellerId} phone verified successfully.")
        
        db.commit()
        logging.info(f"Verification status updated for seller ID {payload.sellerId}.")
        
        return {"message": "Seller verification status updated successfully."}
    except HTTPException as e:
        logging.error(f"HTTP error updating seller status: {str(e)}")
        raise e
    except Exception as e:
        logging.error(f"Error updating seller verification status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")


@router.get("/profile", response_model=SellerBase)
async def fetch_seller_profile():
    return await get_seller_details()

@router.put("/profile")
async def modify_seller_profile(seller: SellerBase):
    return await update_seller_details(seller.dict())

@router.get("/{seller_id}/current-step", response_model=CurrentStepResponse)
def fetch_current_step(seller_id: int, db: Session = Depends(get_db)):
    """Fetch the current registration step for a seller."""
    current_step = get_seller_current_step(db, seller_id)
    if current_step is None:
        raise HTTPException(status_code=404, detail="Seller not found")
    return {"seller_id": seller_id, "current_step": current_step, "registration_data": None}

@router.put("/{seller_id}/current-step", response_model=CurrentStepResponse)
def update_step(request: CurrentStepRequest, db: Session = Depends(get_db)):
    """Update the current registration step for a seller."""
    seller = update_seller_step(db, request.seller_id, request.step, request.registration_data)
    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")
    return {"seller_id": seller.id, "current_step": seller.current_step, "registration_data": seller.registration_data}



@router.post("/send-registration-email")
async def send_registration_email(request: EmailRequest):
    try:
        # Extract email and link from the request body
        email = request.email
        link = request.link

        # Validate the email and link
        if not email or not link:
            raise HTTPException(status_code=400, detail="Email and link are required.")

        # Construct the email content
        subject = "Complete Your Registration"
        body = f"Click on the following link to continue your registration: {link}"

        # Send the email
        send_email(email, subject, body)

        # Log success and return response
        logging.info(f"Email sent to {email} successfully.")
        return {"success": True, "message": "Email sent successfully."}
    except Exception as e:
        logging.error(f"Failed to send email to {request.email}. Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email.")
    
@router.post("/{seller_id}/activity")
def update_seller_activity(seller_id: int):
    try:
        record_seller_activity(seller_id)
        return {"success": True, "message": "Activity updated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update activity.")
    

@router.post("/resend_verification_code")
async def resend_verification_code(data: ResendVerificationCodeRequest, db: Session = Depends(get_db)):
    """
    Resends a verification code for a seller.
    """
    email = data.email
    try:
        # Delegate logic to the service layer
        response = await handle_resend_verification_code(email, db)
        return {"message": response}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")