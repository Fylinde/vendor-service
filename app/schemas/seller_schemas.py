from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import field_validator, model_validator, ValidationInfo
from datetime import datetime

VALID_CURRENCIES = {"USD", "EUR", "GBP", "JPY", "INR", "CAD", "AUD"}  # Example list
VALID_SELLER_TYPES = {"individual", "professional"}  # Valid seller types

class SellerBase(BaseModel):
    full_name: str
    email: EmailStr
    phoneNumber: Optional[str]
    profile_picture: Optional[str] = None
    currency_code: Optional[str] = "USD"  # Default to USD
    seller_type: Optional[str] = None  # Add seller type as optional here

    @model_validator(mode="before")
    def validate_currency_code(cls, values):
        currency_code = values.get("currency_code", "USD")  # Default to "USD" if not provided
        if currency_code not in VALID_CURRENCIES:
            raise ValueError(f"Invalid currency_code: {currency_code}. Must be one of {VALID_CURRENCIES}")
        values["currency_code"] = currency_code
        return values

    class ConfigDict:
        from_attributes = True


class SellerCreate(SellerBase):
    full_name: str
    password: str
    phoneNumber: Optional[str] = None
    profile_picture: Optional[str] = None
    preferences: Optional[str] = None
    verification_code: Optional[str] = None
    verification_expiration: Optional[datetime] = None
    is_email_verified: bool = False
    is_phone_verified: bool = False
    seller_type: str
    currency_code: str

    @field_validator("seller_type")
    def validate_seller_type(cls, v):
        if v not in ["individual", "professional"]:
            raise ValueError("Invalid seller type")
        return v

    @model_validator(mode="before")
    def check_email_or_phone(cls, values):
        email = values.get("email")
        phoneNumber = values.get("phoneNumber")

        if not email and not phoneNumber:
            raise ValueError("Either email or phone number must be provided")

        return values

    class ConfigDict:
        from_attributes = True



class ApprovedSellerResponse(BaseModel):
    sellerId: str
    full_name: str
    email: EmailStr
    phoneNumber: Optional[str] = None
    is_email_verified: bool
    is_phone_verified: bool
    is_approved: bool = True  # At this point, they are approved
    access_token: str  # Access token for dashboard access
    seller_type: str  # Include seller type

    class ConfigDict:
        from_attributes = True


class SellerResponse(BaseModel):
    sellerId: str
    full_name: str
    email: EmailStr
    phoneNumber: Optional[str] = None
    is_email_verified: bool
    is_phone_verified: bool
    is_approved: bool  # Approval status
    verification_sent: bool = True  # Flag to indicate verification email/SMS sent
    seller_type: str  # Include seller type

    class ConfigDict:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class SellerLogin(BaseModel):
    email: Optional[EmailStr] = None
    phoneNumber: Optional[str] = None
    password: str

    @field_validator("phoneNumber", "email", mode="before")
    def validate_email_or_phone(cls, value, info: ValidationInfo):
        email = info.data.get("email")
        phoneNumber = info.data.get("phoneNumber")

        if not email and not phoneNumber:
            raise ValueError("Either 'email' or 'phoneNumber' must be provided.")
        if email and phoneNumber:
            raise ValueError("Provide only one of 'email' or 'phoneNumber', not both.")

        return value


class OTPRequest(BaseModel):
    email: str = None
    phoneNumber: str = None
    carrier_gateway: str = None


class SellerSchema(BaseModel):
    sellerId: str
    full_name: str  # Change to full_name
    email: str
    is_admin: bool
    seller_type: Optional[str] = None  # Optional seller type

    class ConfigDict:
        from_attributes = True


class SellerVerificationResponse(BaseModel):
    sellerId: str
    full_name: str
    email: str
    is_email_verified: bool
    seller_type: str  # Include seller type

    class ConfigDict:
        from_attributes = True


class SellerAuthenticateRequest(BaseModel):
    username: str
    password: str


class SellerAuthenticateResponse(BaseModel):
    sellerId: str
    contact_info: str
    seller_type: str  # Include seller type


class SellerVerificationUpdateRequest(BaseModel):
    sellerId: str
    is_email: bool = True


class CurrentStepRequest(BaseModel):
    sellerId: str
    step: str
    registration_data: Optional[dict] = None


class CurrentStepResponse(BaseModel):
    sellerId: str
    current_step: str
    registration_data: Optional[dict] = None


class EmailRequest(BaseModel):
    email: str
    link: str

class ResendVerificationCodeRequest(BaseModel):
    email: EmailStr  # Validates the email format