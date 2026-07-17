from pydantic import BaseModel, ConfigDict
from typing import Optional


class CustomerCreate(BaseModel):
    full_name: str
    phone: str
    address: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    address: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)