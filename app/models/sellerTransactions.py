from sqlalchemy import Column, Integer, String,  DateTime, Float, ForeignKey
from app.database import BaseModel
from datetime import datetime
from sqlalchemy.orm import relationship


class SellerTransactions(BaseModel):
    __tablename__ = "seller_transactions"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
        # Relationship to SellerModel
    seller = relationship("SellerModel", back_populates="transactions")