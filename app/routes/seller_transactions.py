from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.seller_service import (
    create_seller_transaction_service,
    fetch_seller_transactions_service,
)
from app.schemas.seller_transactions import SellerTransactionCreate, SellerTransactionResponse
from typing import List
from app.models.sellerTransactions import SellerTransactions
router = APIRouter()

@router.post("/payments/escrow", response_model=SellerTransactionResponse)
def initiate_escrow_payment(transaction: SellerTransactionCreate, db: Session = Depends(get_db)):
    try:
        return create_seller_transaction_service(
            db, transaction.seller_id, transaction.transaction_type, transaction.amount
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/escrow/{seller_id}", response_model=List[SellerTransactionResponse])
def get_seller_transactions(seller_id: int, db: Session = Depends(get_db)):
    return fetch_seller_transactions_service(db, seller_id)


@router.post("/escrow")
async def create_transaction(transaction: dict):
    # Mock logic for testing
    if transaction.get("seller_id") and transaction.get("amount"):
        return {"message": "Transaction created"}
    raise HTTPException(status_code=400, detail="Invalid data")

@router.get("/{transaction_id}")
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(SellerTransactions).filter(SellerTransactions.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
