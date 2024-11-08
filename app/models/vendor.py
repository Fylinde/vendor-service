from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import BaseModel
from sqlalchemy import JSON
from datetime import datetime

class VendorModel(BaseModel):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    is_active = Column(Boolean, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(255), nullable=False)
    first_name = Column(String(128), nullable=True)
    middle_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    hashed_password = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)
    jwt_token_key = Column(String, nullable=True)  # <-- Add this column
    password_last_updated = Column(DateTime, nullable=True, default=datetime.utcnow)  # <-- New field
    # Preferences
    preferences = Column(JSON, nullable=True)  # Store user preferences as JSON
    notification_preferences = Column(String, nullable=True)  # Notification preferences
    verification_expiration = Column(DateTime, nullable=True)
    language_code = Column(String(35), default="en")
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)
    date_of_birth = Column(String, nullable=True)  # Store as string for simplicity
    gender = Column(String(10), nullable=True)  # E.g., Male, Female, etc.
    is_email_verified = Column(Boolean, default=False)
    is_phone_verified = Column(Boolean, default=False)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String, nullable=True)
    # New fields for seller dashboard and notifications
    notifications_enabled = Column(Boolean, default=True)  # Enable notifications for sellers
    ai_recommendation_opt_in = Column(Boolean, default=True)  # Sellers can opt in to AI recommendations