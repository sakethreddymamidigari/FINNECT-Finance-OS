"""
Dashboard response schemas.

These schemas define the response structure returned by the
Dashboard API.
"""

from datetime import date
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict

from backend.app.schemas.loan import LoanResponse
from backend.app.schemas.payment import PaymentResponse


class DashboardResponse(BaseModel):
    """
    Response model for the Finance Owner dashboard.
    """

    # -----------------------------
    # Customer Statistics
    # -----------------------------
    total_customers: int

    # -----------------------------
    # Loan Statistics
    # -----------------------------
    active_loans: int
    closed_loans: int

    # -----------------------------
    # Financial Statistics
    # -----------------------------
    total_principal_disbursed: Decimal
    remaining_principal: Decimal
    total_principal_paid: Decimal
    total_interest_paid: Decimal
    today_collection: Decimal

    # -----------------------------
    # Recent Activity
    # -----------------------------
    recent_loans: List[LoanResponse]
    recent_payments: List[PaymentResponse]

    # Enable SQLAlchemy ORM object support
    model_config = ConfigDict(from_attributes=True)

class ProfitSummaryResponse(BaseModel):
    """
    Response model for profit summary.
    """

    total_principal: Decimal
    total_interest: Decimal
    total_amount: Decimal
    loan_count: int

class MaturityLoanResponse(BaseModel):
    """
    Response model for a loan maturing in the selected month.
    """

    loan_id: int
    customer_name: str
    mobile_number: str
    principal_amount: Decimal
    remaining_principal: Decimal
    issue_date: date
    due_date: date
    status: str

    model_config = ConfigDict(from_attributes=True)


class MaturityReportResponse(BaseModel):
    """
    Response model for the maturity report.
    """

    month: int
    year: int
    loan_count: int
    loans: List[MaturityLoanResponse]

class OverdueLoanResponse(BaseModel):
    """
    Response model for an overdue loan.
    """

    loan_id: int
    customer_name: str
    mobile_number: str
    due_date: date
    days_overdue: int
    remaining_principal: Decimal
    status: str

    model_config = ConfigDict(from_attributes=True)


class OverdueLoansResponse(BaseModel):
    """
    Response model for overdue loans report.
    """

    overdue_count: int
    total_overdue_principal: Decimal
    loans: List[OverdueLoanResponse]

class ClosedLoanResponse(BaseModel):
    """
    Response model for a closed loan.
    """

    loan_id: int
    customer_name: str
    mobile_number: str

    principal_amount: Decimal
    total_principal_paid: Decimal
    total_interest_paid: Decimal

    settlement_amount: Decimal | None = None
    waived_amount: Decimal | None = None

    closure_type: str
    closed_date: date | None = None

    model_config = ConfigDict(from_attributes=True)


class ClosedLoansReportResponse(BaseModel):
    """
    Response model for closed loans report.
    """

    loan_count: int
    loans: List[ClosedLoanResponse]