from sqlalchemy.orm import Session
from app.models.seller import SellerModel
from app.models.sellerRatings import SellerRatings



def get_ratings(db: Session, seller_id: int):
    return db.query(SellerModel).filter(SellerModel.id == seller_id).first().ratings



def add_rating(db: Session, seller_id: int, rating_data: dict):
    seller = db.query(SellerModel).filter(SellerModel.id == seller_id).first()
    if seller:
        if not seller.ratings:
            seller.ratings = []
        seller.ratings.append(rating_data)
        db.commit()
        db.refresh(seller)
        return seller.ratings
    return None

# Create a new rating
def create_seller_rating(db: Session, seller_id: int, rating: float, review: str):
    new_rating = SellerRatings(seller_id=seller_id, rating=rating, review=review)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

# Get ratings for a seller
def get_seller_ratings(db: Session, seller_id: int):
    return db.query(SellerRatings).filter(SellerRatings.seller_id == seller_id).all()
