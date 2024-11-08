from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models.vendor import VendorModel
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def cleanup_expired_unverified_users():
    db: Session = SessionLocal()
    try:
        current_time = datetime.utcnow()  # Define current_time here
        expired_users = db.query(VendorModel).filter(
            VendorModel.is_email_verified.is_(False),
            VendorModel.verification_expiration < current_time
        ).all()

        for user in expired_users:
            logger.info(f"Deleting expired unverified user: {user.email}")
            db.delete(user)
        db.commit()
        logger.info("Expired unverified users cleanup complete.")

    except Exception as e:
        logger.error(f"Error during cleanup of expired unverified users: {e}", exc_info=True)

    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_expired_unverified_users, 'interval', minutes=30)  # Set to every 30 minutes or as needed
scheduler.start()
