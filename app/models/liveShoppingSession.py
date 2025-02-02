from sqlalchemy import Column, Integer, DateTime, JSON, ForeignKey
from app.database import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship


class LiveShoppingSession(BaseModel):
    __tablename__ = "live_shopping_sessions"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    session_details = Column(JSON, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    
    
    
        # Relationship to SellerModel
    seller = relationship("SellerModel", back_populates="live_shopping_sessions")