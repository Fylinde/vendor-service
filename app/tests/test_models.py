from app.models.sellerTransactions import SellerTransactions
from app.models.sellerRatings import SellerRatings

def test_create_transaction(db):
    # Create a test transaction
    transaction = SellerTransactions(
        sellerId=1,
        transaction_type="deposit",
        amount=100.0,
        status="pending"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    # Validate the transaction
    assert transaction.id is not None
    assert transaction.sellerId == 1
    assert transaction.amount == 100.0
    assert transaction.status == "pending"

def test_create_seller_rating(db):
    # Create a test rating
    rating = SellerRatings(
        sellerId=1,
        rating=4.5,
        review="Great seller!"
    )
    db.add(rating)
    db.commit()
    db.refresh(rating)

    # Validate the rating
    assert rating.id is not None
    assert rating.rating == 4.5
    assert rating.review == "Great seller!"
