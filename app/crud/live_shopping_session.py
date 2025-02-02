from sqlalchemy.orm import Session
from app.models.liveShoppingSession import LiveShoppingSession

# Create a new live shopping session
def create_live_session(db: Session, seller_id: int, session_details: dict):
    new_session = LiveShoppingSession(seller_id=seller_id, session_details=session_details)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

# Fetch all live shopping sessions
def get_all_live_sessions(db: Session):
    return db.query(LiveShoppingSession).all()

# Fetch live shopping sessions for a specific seller
def get_live_sessions_by_seller(db: Session, seller_id: int):
    return db.query(LiveShoppingSession).filter(LiveShoppingSession.seller_id == seller_id).all()
