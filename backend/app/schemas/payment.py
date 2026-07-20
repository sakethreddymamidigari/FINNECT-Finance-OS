from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PaymentCreate(BaseModel):
    loan_id: int
    payment_date: date
    amount_paid: Decimal
    payment_mode: str
    remarks: Optional[str] = None


class PaymentResponse(BaseModel):
    id: int
    loan_id: int
    finance_owner_id: int
    payment_date: date
    amount_paid: Decimal
    interest_paid: Decimal
    principal_paid: Decimal
    payment_mode: str
    remarks: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)