"""
Finance Owner Schemas

Pydantic models used for request and response validation.
"""

from pydantic import BaseModel, EmailStr


class FinanceOwnerCreate(BaseModel):
    business_name: str
    owner_name: str
    phone: str
    email: EmailStr
    password: str
    address: str


class FinanceOwnerResponse(BaseModel):
    id: int
    business_name: str
    owner_name: str
    phone: str
    email: EmailStr
    address: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str