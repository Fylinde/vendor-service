from pydantic import BaseModel
from typing import Optional

class LiveShoppingSessionBase(BaseModel):
    seller_id: int
    session_details: dict
    started_at: Optional[str] = None
    ended_at: Optional[str] = None

class LiveShoppingSessionCreate(LiveShoppingSessionBase):
    pass

class LiveShoppingSessionResponse(LiveShoppingSessionBase):
    id: int

    class ConfigDict:
       from_attributes = True 
