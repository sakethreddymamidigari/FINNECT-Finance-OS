from decimal import Decimal
from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import and_

from backend.app.models.customer import Customer
from backend.app.models.loan import Loan
from backend.app.models.payment import Payment
from backend.app.schemas.dashboard import (
    DashboardResponse,
    ProfitSummaryResponse,
)


def get_dashboard(
    db: Session,
    finance_owner_id: int,
):
    """
    Return dashboard statistics for the authenticated finance owner.
    """

    # ---------------------------------
    # Customer Statistics
    # ---------------------------------

    total_customers = (
        db.query(Customer)
        .filter(
            Customer.finance_owner_id == finance_owner_id,
        )
        .count()
    )

    # ---------------------------------
    # Loan Statistics
    # ---------------------------------

    active_loans = (
        db.query(Loan)
        .filter(
            Loan.finance_owner_id == finance_owner_id,
            Loan.status == "ACTIVE",
        )
        .count()
    )

    closed_loans = (
        db.query(Loan)
        .filter(
            Loan.finance_owner_id == finance_owner_id,
            Loan.status == "CLOSED",
        )
        .count()
    )

    # ---------------------------------
    # Financial Statistics
    # ---------------------------------

    total_principal_disbursed = (
        db.query(
            func.coalesce(
                func.sum(Loan.principal_amount),
                Decimal("0.00"),
            )
        )
        .filter(
            Loan.finance_owner_id == finance_owner_id,
        )
        .scalar()
    )

    remaining_principal = (
        db.query(
            func.coalesce(
                func.sum(Loan.remaining_principal),
                Decimal("0.00"),
            )
        )
        .filter(
            Loan.finance_owner_id == finance_owner_id,
        )
        .scalar()
    )

    total_principal_paid = (
        db.query(
            func.coalesce(
                func.sum(Loan.total_principal_paid),
                Decimal("0.00"),
            )
        )
        .filter(
            Loan.finance_owner_id == finance_owner_id,
        )
        .scalar()
    )

    total_interest_paid = (
        db.query(
            func.coalesce(
                func.sum(Loan.total_interest_paid),
                Decimal("0.00"),
            )
        )
        .filter(
            Loan.finance_owner_id == finance_owner_id,
        )
        .scalar()
    )

    today_collection = (
        db.query(
            func.coalesce(
                func.sum(Payment.amount_paid),
                Decimal("0.00"),
            )
        )
        .filter(
            Payment.finance_owner_id == finance_owner_id,
            Payment.payment_date == date.today(),
        )
        .scalar()
    )

    # ---------------------------------
    # Recent Activity
    # ---------------------------------

    recent_loans = (
        db.query(Loan)
        .filter(
            Loan.finance_owner_id == finance_owner_id,
        )
        .order_by(Loan.id.desc())
        .limit(5)
        .all()
    )

    recent_payments = (
        db.query(Payment)
        .filter(
            Payment.finance_owner_id == finance_owner_id,
        )
        .order_by(Payment.id.desc())
        .limit(5)
        .all()
    )

    # ---------------------------------
    # Return Dashboard
    # ---------------------------------

    return DashboardResponse(
        total_customers=total_customers,
        active_loans=active_loans,
        closed_loans=closed_loans,
        total_principal_disbursed=total_principal_disbursed,
        remaining_principal=remaining_principal,
        total_principal_paid=total_principal_paid,
        total_interest_paid=total_interest_paid,
        today_collection=today_collection,
        recent_loans=recent_loans,
        recent_payments=recent_payments,
    )

def get_profit_summary(
    db: Session,
    finance_owner_id: int,
    from_date: date,
    to_date: date,
):
    """
    Return profit summary for the selected period.
    """

    loans = (
        db.query(Loan)
        .filter(
            Loan.finance_owner_id == finance_owner_id,
            Loan.issue_date >= from_date,
            Loan.issue_date <= to_date,
        )
        .all()
    )

    total_principal = Decimal("0.00")
    total_interest = Decimal("0.00")

    for loan in loans:
        total_principal += loan.principal_amount
        total_interest += loan.total_interest_paid

    return ProfitSummaryResponse(
        total_principal=total_principal,
        total_interest=total_interest,
        total_amount=total_principal + total_interest,
        loan_count=len(loans),
    )