from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.ratings import get_ratings, add_rating
from app.schemas.ratings import Rating, RatingResponse
from app.database import get_db

from app.services.seller_service import add_seller_rating_service, fetch_seller_ratings_service
from app.schemas.ratings import SellerRatingCreate, SellerRatingResponse
from typing import List


router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.get("/{seller_id}", response_model=RatingResponse)
async def fetch_ratings(seller_id: int, db: Session = Depends(get_db)):
    return get_ratings(db, seller_id)

@router.post("/{seller_id}")
async def add_new_rating(seller_id: int, rating: Rating, db: Session = Depends(get_db)):
    return add_rating(db, seller_id, rating.dict())


@router.post("/sellers/{seller_id}/ratings", response_model=SellerRatingResponse)
def add_seller_rating(seller_id: int, rating: SellerRatingCreate, db: Session = Depends(get_db)):
    return add_seller_rating_service(db, seller_id, rating.rating, rating.review)

@router.get("/sellers/{seller_id}/ratings", response_model=List[SellerRatingResponse])
def get_seller_ratings(seller_id: int, db: Session = Depends(get_db)):
    return fetch_seller_ratings_service(db, seller_id)