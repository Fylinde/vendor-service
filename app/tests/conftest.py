import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import BaseModel
from app.config import settings
from app.models import SellerModel


# Use the test database URL from settings
DATABASE_URL = settings.effective_database_url
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print(f"Using database URL: {DATABASE_URL}")

@pytest.fixture(scope="module")
def db():
    # Create tables and seed initial data
    BaseModel.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    # Seed the sellers table
    seller = SellerModel(id=1, full_name="Test Seller", email="test@example.com", hashed_password="hashed")
    session.add(seller)
    session.commit()

    yield session

    session.close()
    BaseModel.metadata.drop_all(bind=engine)
