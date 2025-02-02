from sqlalchemy.orm import Session
from app.models.sellerTransactions import SellerTransactions

# Create a new transaction
def create_transaction(db: Session, seller_id: int, transaction_type: str, amount: float, status: str = "pending"):
    new_transaction = SellerTransactions(
        seller_id=seller_id,
        transaction_type=transaction_type,
        amount=amount,
        status=status
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

# Get transactions for a specific seller
def get_transactions_by_seller(db: Session, seller_id: int):
    return db.query(SellerTransactions).filter(SellerTransactions.seller_id == seller_id).all()
