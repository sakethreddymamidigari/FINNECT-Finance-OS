from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict


class LoanRenewalCreate(BaseModel):
    renewal_type: Literal[
        "CONTINUE",
        "CAPITALIZE",
    ]

    new_due_date: date

    interest_method: Literal[
        "PERCENTAGE",
        "RUPEES_PER_100",
    ]

    interest_rate: Decimal

    remarks: str | None = None


class LoanRenewalResponse(BaseModel):
    id: int

    old_loan_id: int
    new_loan_id: int | None = None

    finance_owner_id: int

    renewal_type: str

    old_due_date: date
    new_due_date: date

    old_interest_method: str
    new_interest_method: str

    old_interest_rate: Decimal
    new_interest_rate: Decimal

    remaining_principal: Decimal
    outstanding_interest: Decimal
    new_principal: Decimal

    remarks: str | None = None

    renewed_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )