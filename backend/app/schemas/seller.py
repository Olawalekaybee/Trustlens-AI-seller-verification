from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SellerBase(BaseModel):
    seller_name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    business_name: Optional[str] = None
    social_handle: Optional[str] = None
    bank_account_name: Optional[str] = None


class SellerCreate(SellerBase):
    pass


class SellerResponse(SellerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True