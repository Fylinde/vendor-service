from fastapi import HTTPException, status
import requests
from sqlalchemy.orm import Session
from app.crud.seller_crud import create_seller, get_seller_by_email, get_seller_by_phone, get_current_step, update_current_step
from app.schemas.seller_schemas import SellerCreate
from app.config import settings
import logging
from app.utils.http_client import http_client
from app.models.seller import SellerModel
from app.crud.ratings import create_seller_rating, get_seller_ratings
from app.crud.live_shopping_session import (
    create_live_session,
    get_all_live_sessions,
    get_live_sessions_by_seller,
)
from app.crud.seller_transactions import create_transaction, get_transactions_by_seller
from app.crud.seller_crud import update_last_activity
from app.database import SessionLocal
from app.clients.auth_service_client import AuthServiceClient
from tenacity import retry, stop_after_attempt, wait_fixed

logger = logging.getLogger(__name__)


AUTH_SERVICE_URL = settings.AUTH_SERVICE_URL
BASE_API_URL = "https://api.example.com"

# Retry logic: If the request to auth-service fails, retry up to 3 times with a 2-second delay
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def send_verification_payload(payload):
    logging.info(f"[send_verification_payload] Sending verification payload: {payload}")
    response = requests.post(f"{AUTH_SERVICE_URL}/generate-verification-code", json=payload)
    response.raise_for_status()  # Raise an error for HTTP 4xx or 5xx responses
    return response.json()

# def register_seller(db: Session, seller_data: SellerCreate):
#     try:
#         logging.info("[register_seller] Starting seller registration process.")
#         logging.info(f"[register_seller] Input Data: {seller_data.dict()}")

#         seller_data.currency_code = seller_data.currency_code or "USD"
#         logging.info(f"[register_seller] Currency code set to: {seller_data.currency_code}")

#         if seller_data.seller_type not in ["professional", "individual"]:
#             logging.error(f"[register_seller] Invalid seller type: {seller_data.seller_type}")
#             raise HTTPException(status_code=400, detail="Invalid seller type. Must be 'professional' or 'individual'.")

#         logging.info(f"[register_seller] Seller type validated: {seller_data.seller_type}")

#         existing_seller = (
#             db.query(SellerModel)
#             .filter((SellerModel.email == seller_data.email) | (SellerModel.phoneNumber == seller_data.phoneNumber))
#             .first()
#         )
#         if existing_seller:
#             logging.error("[register_seller] Seller already exists with the same email or phone number.")
#             raise HTTPException(status_code=400, detail="Email or phone number already registered")

#         logging.info("[register_seller] Creating unverified and unapproved seller in the database.")
#         seller = create_seller(db, seller_data, is_verified=False, is_approved=False)
#         db.refresh(seller)
#         logging.info(f"[register_seller] Seller created successfully with ID: {seller.id}")

#         verification_payload = {
#             "contact": seller_data.email or seller_data.phoneNumber,
#             "is_email": bool(seller_data.email),
#             "seller_type": seller.seller_type,
#             "sellerId": str(seller.id),
#         }
#         logging.info(f"[register_seller] Verification payload prepared: {verification_payload}")

#         try:
#             logging.info(f"[register_seller] Sending payload to auth-service: {verification_payload}")
#             verification_data = send_verification_payload(verification_payload)

#             if "verification_code" not in verification_data:
#                 logging.error(f"[register_seller] Auth-service response missing verification code: {verification_data}")
#                 raise HTTPException(status_code=500, detail="Unexpected response from auth service")

#             logging.info(f"[register_seller] Verification code received from auth-service: {verification_data['verification_code']}")

#         except requests.RequestException as e:
#             logging.error(f"[register_seller] Auth-service connection error: {e}")
#             raise HTTPException(status_code=500, detail="Failed to connect to auth service")

#         response = {
#             "sellerId": str(seller.id),
#             "full_name": seller.full_name,
#             "email": seller.email,
#             "verification_code": verification_data["verification_code"],
#             "phoneNumber": seller.phoneNumber,
#             "seller_type": seller.seller_type,
#             "verification_sent": True,
#             "is_approved": seller.is_approved,
#             "is_email_verified": seller.is_email_verified,
#             "is_phone_verified": seller.is_phone_verified,
#         }
#         logging.info(f"[register_seller] Final response prepared: {response}")
#         return response

#     except Exception as e:
#         logging.error(f"[register_seller] Unexpected error: {e}", exc_info=True)
#         raise HTTPException(status_code=500, detail="Failed to register seller due to an unexpected error")

def register_seller(db: Session, seller_data: SellerCreate):
    """
    Registers an unverified seller, creates a verification payload, and sends an API request to generate a verification code.
    
    Parameters:
    - db (Session): Database session instance.
    - seller_data (SellerCreate): Seller creation schema containing necessary seller details.
    
    Returns:
    - dict: Response containing seller details and verification status.
    """
    logging.info("Starting seller registration process.")
    
    try:
        # Step 1: Create a new seller instance using create_seller()
        seller = create_seller(db, seller_data, is_verified=False, is_approved=False)
        logging.info(f"Seller created successfully with ID: {seller.id}")
        
        # Step 2: Prepare the verification payload
        verification_payload = {
            "contact": seller.email or seller.phoneNumber,
            "is_email": bool(seller.email),
            "seller_type": seller.seller_type,
            "sellerId": str(seller.id),
        }
        logging.info("Verification payload prepared: %s", verification_payload)
        
        # Step 3: Send request to AUTH_SERVICE to generate verification code
        verification_url = f"{AUTH_SERVICE_URL}/generate-verification-code"
        logging.info(f"Sending verification request to: {verification_url}")
        
        try:
            response = requests.post(verification_url, json=verification_payload)
            response.raise_for_status()  # Raises HTTPError for bad responses
            verification_data = response.json()
            logging.info("Verification code received successfully.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send verification request: {str(e)}")
            return {"error": "Failed to generate verification code", "details": str(e)}
        
        # Step 4: Construct final response
        result = {
            "sellerId": str(seller.id),
            "full_name": seller.full_name,
            "email": seller.email,
            "verification_code": verification_data.get("verification_code"),
            "phoneNumber": seller.phoneNumber,
            "seller_type": seller.seller_type,
            "verification_sent": True,
            "is_approved": seller.is_approved,
            "is_email_verified": seller.is_email_verified,
            "is_phone_verified": seller.is_phone_verified,
        }
        logging.info("Seller Verification Data Is Successfully Sent.")
        
        return result
    
    except Exception as e:
        logging.error(f"An error occurred during seller registration: {str(e)}")
        db.rollback()  # Rollback in case of failure
        return {"error": "Seller registration failed", "details": str(e)}


async def get_seller_rating(sellerId: str):
    response = await http_client.get(f"{BASE_API_URL}/sellers/{sellerId}/ratings")
    return response.json()

async def add_seller_rating(sellerId: str, rating_data: dict):
    response = await http_client.post(f"{BASE_API_URL}/sellers/{sellerId}/ratings", json=rating_data)
    return response.json()

async def get_seller_details():
    response = await http_client.get(f"{BASE_API_URL}/sellers/profile")
    return response.json()

async def update_seller_details(data: dict):
    response = await http_client.put(f"{BASE_API_URL}/sellers/profile", json=data)
    return response.json()

def get_seller_current_step(db: Session, sellerId: str):
    """Service to get the current registration step."""
    return get_current_step(db, sellerId)

def update_seller_step(db: Session, sellerId: str, step: str, registration_data: dict = None):
    """Service to update the current registration step."""
    return update_current_step(db, sellerId, step, registration_data)


def add_seller_rating_service(db: Session, sellerId: str, rating: float, review: str):
    return create_seller_rating(db, sellerId, rating, review)

def fetch_seller_ratings_service(db: Session, sellerId: str):
    return get_seller_ratings(db, sellerId)



# Add a new live shopping session
def create_live_shopping_session_service(db: Session, sellerId: str, session_details: dict):
    return create_live_session(db, sellerId, session_details)

# Fetch all live shopping sessions
def fetch_all_live_shopping_sessions_service(db: Session):
    return get_all_live_sessions(db)

# Fetch live shopping sessions for a specific seller
def fetch_live_sessions_by_seller_service(db: Session, sellerId: str):
    return get_live_sessions_by_seller(db, sellerId)


# Create a new transaction
def create_seller_transaction_service(db: Session, sellerId: str, transaction_type: str, amount: float):
    return create_transaction(db, sellerId, transaction_type, amount)

# Fetch all transactions for a specific seller
def fetch_seller_transactions_service(db: Session, sellerId: str):
    return get_transactions_by_seller(db, sellerId)

def record_seller_activity(sellerId: str):
    db = SessionLocal()
    try:
        update_last_activity(sellerId, db)
    finally:
        db.close()
        

async def handle_resend_verification_code(email: str, db: Session) -> str:
    """
    Handles the logic for resending a verification code for a seller.
    """
    logger.info(f"Attempting to resend verification code for email: {email}")

    # Validate the seller exists in the database
    seller = db.query(SellerModel).filter(SellerModel.email == email).first()
    if not seller:
        logger.warning(f"No seller found with email: {email}")
        raise HTTPException(status_code=404, detail="Seller not found.")
    if seller.is_email_verified:
        logger.warning(f"Email {email} is already verified.")
        raise HTTPException(status_code=400, detail="Email is already verified.")

    # Prepare payload for auth-service
    payload = {
        "sellerId": str(seller.id),
        "contact": seller.email,
        "seller_type": seller.seller_type
    }

    # Make the API call to auth-service
    auth_client = AuthServiceClient()
    try:
        response = await auth_client.resend_verification_code(payload)
        logger.info(f"Auth-service response: {response}")
        return response["message"]
    except Exception as e:
        logger.error(f"Failed to contact auth-service: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to contact auth-service: {e}")
