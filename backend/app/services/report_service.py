from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.models.payment import Payment


def get_profit_report(
    db: Session,
    start_date,
    end_date,
):
    """
    Returns collection statistics for the given date range.

    Calculations are based on the payments table.
    """

    result = (
        db.query(
            func.coalesce(func.sum(Payment.principal_paid), Decimal("0.00")).label(
                "total_principal_collected"
            ),
            func.coalesce(func.sum(Payment.interest_paid), Decimal("0.00")).label(
                "total_interest_collected"
            ),
            func.count(Payment.id).label("payment_count"),
        )
        .filter(
            Payment.payment_date >= start_date,
            Payment.payment_date <= end_date,
        )
        .first()
    )

    total_principal = result.total_principal_collected or Decimal("0.00")
    total_interest = result.total_interest_collected or Decimal("0.00")
    payment_count = result.payment_count or 0

    total_collection = total_principal + total_interest

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_principal_collected": total_principal,
        "total_interest_collected": total_interest,
        "total_collection": total_collection,
        "payment_count": payment_count,
    }