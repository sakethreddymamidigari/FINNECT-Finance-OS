from pydantic import BaseModel, EmailStr


class FinanceOwnerCreate(BaseModel):
    business_name: str
    owner_name: str
    phone: str
    email: EmailStr
    password: str
    address: str