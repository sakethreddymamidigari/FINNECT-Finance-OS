from datetime import date
from decimal import Decimal
from typing import List
from pydantic import BaseModel, ConfigDict


class LoanCreate(BaseModel):
    customer_id: int
    principal_amount: Decimal
    interest_method: str
    interest_rate: Decimal
    issue_date: date
    due_date: date

class LoanUpdate(BaseModel):
    interest_method: str
    interest_rate: Decimal
    due_date: date

class LoanResponse(BaseModel):
    id: int
    customer_id: int
    principal_amount: Decimal
    remaining_principal: Decimal
    total_principal_paid: Decimal
    total_interest_paid: Decimal
    interest_method: str
    interest_rate: Decimal
    issue_date: date
    due_date: date
    interest_start_date: date
    last_interest_calculated_on: date
    status: str

    model_config = ConfigDict(from_attributes=True)

class LoanStatementPaymentResponse(BaseModel):
    """
    Payment details for the loan statement.
    """

    payment_date: date
    amount_paid: Decimal
    principal_paid: Decimal
    interest_paid: Decimal
    payment_mode: str
    remarks: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LoanStatementResponse(BaseModel):
    """
    Complete statement for a single loan.
    """

    loan: LoanResponse
    customer_name: str
    customer_phone: str
    accrued_interest: Decimal
    total_outstanding: Decimal
    payments: List[LoanStatementPaymentResponse]