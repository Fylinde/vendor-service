from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config import settings
from app.utils.email_service import send_email
import os
import logging
from datetime import datetime, timedelta

INACTIVITY_THRESHOLD_MINUTES = 5  # Adjust as needed (e.g., 30 for production)

# Base class for models
BaseModel = declarative_base()

# Main production database URL
SQLALCHEMY_DATABASE_URL = settings.effective_database_url

# Define a test database URL (set this URL in your environment variables)
TEST_SQLALCHEMY_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql+psycopg2://postgres:Sylvian@db:5433/test_vendor_service_db"
)

# Create a test engine and session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(TEST_SQLALCHEMY_DATABASE_URL))
# Conditionally select the correct database URL
is_testing = os.getenv("TESTING", "0") == "1"  # TESTING=1 indicates test mode
database_url = TEST_SQLALCHEMY_DATABASE_URL if is_testing else SQLALCHEMY_DATABASE_URL

# Create engine for the selected database
engine = create_engine(database_url, connect_args={"check_same_thread": False} if "sqlite" in database_url else {})

# Session factory for production or testing
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency to provide a database session for routes and services.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_inactive_sellers():
    # Import SellerModel here to avoid circular dependency
    from app.models.seller import SellerModel

    db: Session = SessionLocal()
    try:
        # Calculate the inactivity threshold
        inactivity_threshold = datetime.utcnow() - timedelta(minutes=INACTIVITY_THRESHOLD_MINUTES)

        # Query sellers who have been inactive beyond the threshold
        inactive_sellers = db.query(SellerModel).filter(SellerModel.last_activity < inactivity_threshold).all()

        # Notify each inactive seller
        for seller in inactive_sellers:
            if seller.email:
                try:
                    # Construct the email content
                    subject = "We Miss You!"
                    body = (
                        f"Dear {seller.full_name},\n\n"
                        f"We noticed that you haven't completed your registration process. "
                        f"Please click the link below to continue:\n"
                        f"{seller.current_step_link}\n\n"
                        f"Thank you,\nThe Team"
                    )

                    # Send the email
                    send_email(seller.email, subject, body)
                    logging.info(f"Notification sent to inactive seller: {seller.email}")
                except Exception as e:
                    logging.error(f"Failed to send email to {seller.email}: {e}")
            else:
                logging.warning(f"Seller {seller.id} has no email on record. Skipping notification.")

    except Exception as e:
        logging.error(f"Error checking inactive sellers: {e}")
    finally:
        db.close()
