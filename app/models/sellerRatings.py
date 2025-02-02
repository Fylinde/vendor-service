from sqlalchemy import Column, Integer, String,  DateTime, Float, ForeignKey
from app.database import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship

class SellerRatings(BaseModel):
    __tablename__ = "seller_ratings"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    rating = Column(Float, nullable=False)
    review = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
        # Relationship to SellerModel
    seller = relationship("SellerModel", back_populates="ratings")