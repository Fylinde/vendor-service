from pydantic import BaseModel, EmailStr, Field

class VendorBase(BaseModel):
    name: str
    description: str = None

class VendorCreate(VendorBase):
    email: EmailStr
    password: str = Field(..., min_length=6)

class VendorResponse(VendorBase):
    id: int
    is_active: bool
    email: EmailStr

    class Config:
        orm_mode = True
