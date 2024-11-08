import requests
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud.vendor_crud import create_vendor, get_vendor_by_email
from app.schemas.vendor_schemas import VendorCreate
from app.rabbitmq.rabbitmq_publisher import publish_vendor_created_event


AUTH_SERVICE_URL = "http://auth-service-url"  # Replace with actual auth-service URL

def register_vendor(db: Session, vendor_data: VendorCreate):
    # Check if vendor with the same email already exists
    existing_vendor = get_vendor_by_email(db, vendor_data.email)
    if existing_vendor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create vendor in vendor database
    vendor = create_vendor(db, vendor_data)
    
    # Call auth-service to create credentials
    auth_payload = {
        "email": vendor_data.email,
        "password": vendor_data.password
    }
    auth_response = requests.post(f"{AUTH_SERVICE_URL}/create_user", json=auth_payload)
    if auth_response.status_code != 201:
        db.delete(vendor)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create credentials in auth service"
        )

    # Publish vendor created event to RabbitMQ
    publish_vendor_created_event(vendor)

    return vendor
