from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class LoanCreate(BaseModel):
    customer_id: int
    principal_amount: Decimal
    interest_method: str
    interest_rate: Decimal
    issue_date: date
    due_date: date


class LoanResponse(BaseModel):
    id: int
    customer_id: int
    principal_amount: Decimal
    interest_method: str
    interest_rate: Decimal
    issue_date: date
    due_date: date
    status: str

    model_config = ConfigDict(from_attributes=True)