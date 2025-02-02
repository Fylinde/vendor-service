from fastapi.testclient import TestClient
from app.main import app
from app.models.sellerTransactions import SellerTransactions

client = TestClient(app)

def test_create_transaction(db):
    # Create a transaction
    transaction = SellerTransactions(
        sellerId=1,  # Matches seeded seller
        transaction_type="deposit",
        amount=100.0,
        status="pending"
    )
    db.add(transaction)
    db.commit()
    assert transaction.id is not None


def test_get_transactions_endpoint(db):
    # Create a transaction in the test database
    transaction = SellerTransactions(
        sellerId=1,  # Make sure this seller exists in the test DB
        transaction_type="deposit",
        amount=100.0,
        status="pending"
    )
    db.add(transaction)
    db.commit()

    # Fetch the transaction ID
    transaction_id = transaction.id

    # Test the endpoint
    response = client.get(f"/payments/escrow/{transaction_id}")
    assert response.status_code == 200
    assert response.json()["id"] == transaction_id

