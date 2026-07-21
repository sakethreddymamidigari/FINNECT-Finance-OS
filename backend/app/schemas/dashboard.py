"""
Dashboard response schemas.

These schemas define the response structure returned by the
Dashboard API.
"""

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