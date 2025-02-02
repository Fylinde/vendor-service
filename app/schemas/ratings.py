from pydantic import BaseModel
from typing import List, Optional

class Rating(BaseModel):
    rating: float
    review: Optional[str] = None
    reviewer: str

class RatingResponse(BaseModel):
    average: float
    count: int
    reviews: List[Rating]
    

class SellerRatingBase(BaseModel):
    seller_id: int
    rating: float
    review: Optional[str] = None

class SellerRatingCreate(SellerRatingBase):
    pass

class SellerRatingResponse(SellerRatingBase):
    id: int

    class ConfigDict:
       from_attributes = True 
