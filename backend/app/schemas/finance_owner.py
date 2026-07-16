from pydantic import BaseModel, EmailStr


class FinanceOwnerCreate(BaseModel):
    business_name: str
    owner_name: str
    phone: str
    email: EmailStr
    password: str
    address: str

class FinanceOwnerResponse(BaseModel):
    id:int
    business_name: str
    owner_name: str
    phone: str
    email: EmailStr
    address: str

    class Config:
        from_attribute = True
        
class FinanceOwnerLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str