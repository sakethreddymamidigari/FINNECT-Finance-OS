from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from backend.app.models.enums import PaymentMode


class LoanSettlementPreviewResponse(BaseModel):
    # Loan information
    loan_id: int
    customer_name: str

    # Outstanding amounts before settlement
    principal_outstanding: Decimal
    interest_outstanding: Decimal
    total_outstanding: Decimal


class LoanSettlementRequest(BaseModel):
    # Final negotiated amount agreed with the customer
    settlement_amount: Decimal = Field(..., gt=0)

    # Date on which the settlement is completed
    settlement_date: date

    payment_mode: PaymentMode
    # Optional reason for settling the loan
    settlement_reason: str | None = Field(
        default=None,
        max_length=255,
    )


class LoanSettlementResponse(BaseModel):
    # Settlement confirmation
    message: str

    loan_id: int

    settlement_amount: Decimal
    waived_amount: Decimal

    closure_type: str
    status: str