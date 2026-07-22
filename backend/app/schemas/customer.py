from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from decimal import Decimal
from datetime import date, datetime


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

class CustomerListResponse(BaseModel):
    id: int
    full_name: str

    class Config:
        from_attributes = True

class CustomerLedgerPaymentResponse(BaseModel):
    """
    Payment details for a loan.
    """

    payment_date: date
    amount_paid: Decimal
    principal_paid: Decimal
    interest_paid: Decimal
    payment_mode: str
    remarks: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CustomerLedgerLoanResponse(BaseModel):
    """
    Loan details along with payment history.
    """

    loan_id: int
    principal_amount: Decimal
    remaining_principal: Decimal
    total_principal_paid: Decimal
    total_interest_paid: Decimal
    accrued_interest: Decimal
    total_outstanding: Decimal
    issue_date: date
    due_date: date
    status: str
    payments: List[CustomerLedgerPaymentResponse]


class CustomerLedgerSummaryResponse(BaseModel):
    """
    Overall summary of the customer's loans.
    """

    total_loans: int
    active_loans: int
    closed_loans: int
    total_principal: Decimal
    remaining_principal: Decimal
    total_interest_paid: Decimal
    accrued_interest: Decimal
    total_outstanding: Decimal


class CustomerLedgerResponse(BaseModel):
    """
    Complete customer ledger.
    """

    customer: CustomerResponse
    summary: CustomerLedgerSummaryResponse
    loans: List[CustomerLedgerLoanResponse]