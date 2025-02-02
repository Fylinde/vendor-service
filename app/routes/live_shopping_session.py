from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.seller_service import (
    create_live_shopping_session_service,
    fetch_all_live_shopping_sessions_service,
    fetch_live_sessions_by_seller_service,
)
from app.schemas.live_shopping_session import LiveShoppingSessionCreate, LiveShoppingSessionResponse
from typing import List


router = APIRouter()

@router.post("/live-shopping/start", response_model=LiveShoppingSessionResponse)
def start_live_session(seller_id: int, session: LiveShoppingSessionCreate, db: Session = Depends(get_db)):
    try:
        return create_live_shopping_session_service(db, seller_id, session.session_details)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/live-shopping/sessions", response_model=List[LiveShoppingSessionResponse])
def get_all_live_sessions(db: Session = Depends(get_db)):
    return fetch_all_live_shopping_sessions_service(db)

@router.get("/live-shopping/sessions/{seller_id}", response_model=List[LiveShoppingSessionResponse])
def get_live_sessions_by_seller(seller_id: int, db: Session = Depends(get_db)):
    return fetch_live_sessions_by_seller_service(db, seller_id)
