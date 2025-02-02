from pydantic import BaseModel
from typing import Optional

class SellerTransactionBase(BaseModel):
    seller_id: int
    transaction_type: str
    amount: float
    status: Optional[str] = "pending"

class SellerTransactionCreate(SellerTransactionBase):
    pass

class SellerTransactionResponse(SellerTransactionBase):
    id: int
    created_at: str

    class ConfigDict:
        from_attributes = True 
