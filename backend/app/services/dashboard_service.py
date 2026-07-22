from decimal import Decimal
from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import and_

from backend.app.models.customer import Customer
from backend.app.models.loan import Loan
from backend.app.models.payment import Payment
from backend.app.utils.interest_calculator import calculate_interest
from backend.app.schemas.dashboard import (
    DashboardResponse,
    ProfitSummaryResponse,
    MaturityLoanResponse,
    MaturityReportResponse,
    OverdueLoanResponse,
    OverdueLoansResponse,
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
    Return the profit summary for the selected date range.

    Interest is calculated dynamically up to today so the
    report always reflects the latest accrued amount.
    """

    # Fetch all loans issued within the selected period.
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

    today = date.today()

    # Calculate the latest accrued interest for every loan.
    for loan in loans:

        total_principal += loan.principal_amount

        accrued_interest = calculate_interest(
            principal=loan.remaining_principal,
            rate=loan.interest_rate,
            method=loan.interest_method,
            start_date=loan.last_interest_calculated_on,
            end_date=today,
        )

        # Add both collected interest and currently accrued interest.
        total_interest += (
            loan.total_interest_paid +
            accrued_interest
        )

    return ProfitSummaryResponse(
        total_principal=total_principal,
        total_interest=total_interest,
        total_amount=total_principal + total_interest,
        loan_count=len(loans),
    )

def get_maturity_report(
    db: Session,
    finance_owner_id: int,
    month: int,
    year: int,
):
    """
    Return all loans maturing in the selected month and year.
    """

    loans = (
        db.query(Loan, Customer)
        .join(
            Customer,
            Loan.customer_id == Customer.id,
        )
        .filter(
            Loan.finance_owner_id == finance_owner_id,
            func.extract("month", Loan.due_date) == month,
            func.extract("year", Loan.due_date) == year,
        )
        .order_by(Loan.due_date.asc())
        .all()
    )

    maturity_loans = []

    for loan, customer in loans:
        maturity_loans.append(
            MaturityLoanResponse(
                loan_id=loan.id,
                customer_name=customer.full_name,
                mobile_number=customer.phone,
                principal_amount=loan.principal_amount,
                remaining_principal=loan.remaining_principal,
                issue_date=loan.issue_date,
                due_date=loan.due_date,
                status=loan.status,
            )
        )

    return MaturityReportResponse(
        month=month,
        year=year,
        loan_count=len(maturity_loans),
        loans=maturity_loans,
    )

def get_overdue_loans(
    db: Session,
    finance_owner_id: int,
):
    """
    Return all overdue active loans for the authenticated
    finance owner.
    """

    today = date.today()

    loans = (
        db.query(Loan, Customer)
        .join(
            Customer,
            Loan.customer_id == Customer.id,
        )
        .filter(
            Loan.finance_owner_id == finance_owner_id,
            Loan.status == "ACTIVE",
            Loan.due_date < today,
        )
        .order_by(Loan.due_date.asc())
        .all()
    )

    overdue_loans = []
    total_overdue_principal = Decimal("0.00")

    for loan, customer in loans:

        total_overdue_principal += loan.remaining_principal

        overdue_loans.append(
            OverdueLoanResponse(
                loan_id=loan.id,
                customer_name=customer.full_name,
                mobile_number=customer.phone,
                due_date=loan.due_date,
                days_overdue=(today - loan.due_date).days,
                remaining_principal=loan.remaining_principal,
                status=loan.status,
            )
        )

    return OverdueLoansResponse(
        overdue_count=len(overdue_loans),
        total_overdue_principal=total_overdue_principal,
        loans=overdue_loans,
    )