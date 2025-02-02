from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime, JSON, Float
from app.database import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy import event


class SellerModel(BaseModel):
    __tablename__ = "sellers"

    # Basic Seller Information
    id = Column(Integer, primary_key=True, index=True)
    sellerId = Column(String, ForeignKey("sellers.id"), nullable=True)
    full_name = Column(String(255), nullable=False)  # Seller's full name
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phoneNumber = Column(String(20), nullable=True)
    profile_picture = Column(String, nullable=True)
    seller_type = Column(String, nullable=False)
     
    # Registration and Progress Tracking
    current_step = Column(String(50), nullable=True, default="email_verification")  # Tracks the current step in the registration process
    registration_data = Column(JSON, nullable=True)  # Stores incomplete registration data for resuming
    verification_code = Column(String, nullable=True)
    verification_expiration = Column(DateTime, nullable=True)

    # Preferences and Localization
    preferences = Column(JSON, nullable=True)
    notification_preferences = Column(String, nullable=True)
    language_code = Column(String(35), default="en")  # Default language
    currency_code = Column(String(10), default="USD")  # Default currency

    # Advanced Features
    ai_recommendation_opt_in = Column(Boolean, default=True)  # Opt-in for AI recommendations
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String, nullable=True)
    notifications_enabled = Column(Boolean, default=True)
    
    # Verification and Status
    is_email_verified = Column(Boolean, default=False)
    is_phone_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    lastActivityTimestamp = Column(DateTime, default=datetime.utcnow)  # Track last activity
    is_admin = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)  # Admin approval for seller activation

    # Escrow and Payment Integration
    escrow_balance = Column(Float, default=0.0)  # Escrow account balance

    # Timestamps and Metadata
    password_last_updated = Column(DateTime, nullable=True, default=datetime.utcnow)
    date_of_birth = Column(String, nullable=True)
    gender = Column(String(10), nullable=True)
    last_login = Column(DateTime, nullable=True)  # Tracks the last login time
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # JWT and Authentication
    jwt_token_key = Column(String, nullable=True)

    # Multi-Currency and Exchange Support
    exchange_rates = Column(JSON, nullable=True)  # Stores exchange rates for multi-currency pricing


    # One-to-Many relationship with SellerRatings
    ratings = relationship("SellerRatings", back_populates="seller")
    
    
        # One-to-Many relationship with LiveShoppingSession
    live_shopping_sessions = relationship("LiveShoppingSession", back_populates="seller")
    
    
        # One-to-Many relationship with SellerTransactions
    transactions = relationship("SellerTransactions", back_populates="seller")
    
    