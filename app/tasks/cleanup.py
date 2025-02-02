from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models.seller import SellerModel
import logging
from app.crud.seller_crud import deactivate_inactive_sellers
from app.utils.email_service import send_email
from datetime import  timedelta
from celery import Celery

celery = Celery("tasks", broker="redis://localhost:6379/0")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery.task
def check_and_notify_inactive_sellers():
    db = SessionLocal()
    try:
        # Notify inactive sellers
        threshold_minutes = 25
        notify_time = datetime.utcnow() - timedelta(minutes=threshold_minutes)
        sellers_to_notify = db.query(SellerModel).filter(SellerModel.lastActivityTimestamp < notify_time, SellerModel.is_active == True).all()
        for seller in sellers_to_notify:
            send_email(
                to_email=seller.email,
                subject="We Miss You!",
                body=f"Hi {seller.name}, we noticed you haven't been active. Complete your registration or interact with your account to stay active."
            )

        # Deactivate sellers past the threshold
        deactivate_inactive_sellers(db, threshold_minutes=30)
    finally:
        db.close()

def cleanup_expired_unverified_users():
    db: Session = SessionLocal()
    try:
        current_time = datetime.utcnow()  # Define current_time here
        expired_users = db.query(SellerModel).filter(
            SellerModel.is_email_verified.is_(False),
            SellerModel.verification_expiration < current_time
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
