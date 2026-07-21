from datetime import date
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.app.models.customer import Customer
from backend.app.models.loan import Loan
from backend.app.schemas.loan import LoanCreate, LoanUpdate


def create_loan(
    db: Session,
    loan: LoanCreate,
    finance_owner_id: int,
):
    customer = (
        db.query(Customer)
        .filter(
            Customer.id == loan.customer_id,
            Customer.finance_owner_id == finance_owner_id,
        )
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )

    db_loan = Loan(
        finance_owner_id=finance_owner_id,
        customer_id=loan.customer_id,
        principal_amount=loan.principal_amount,
        remaining_principal=loan.principal_amount,
        total_principal_paid=Decimal("0.00"),
        total_interest_paid=Decimal("0.00"),
        interest_method=loan.interest_method,
        interest_rate=loan.interest_rate,
        issue_date=loan.issue_date,
        due_date=loan.due_date,
        interest_start_date=loan.issue_date,
        last_interest_calculated_on=loan.issue_date,
        status="ACTIVE",
    )

    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)

    return db_loan


def get_loans(
    db: Session,
    finance_owner_id: int,
):
    return (
        db.query(Loan)
        .filter(
            Loan.finance_owner_id == finance_owner_id
        )
        .all()
    )


def get_loan_by_id(
    db: Session,
    loan_id: int,
    finance_owner_id: int,
):
    loan = (
        db.query(Loan)
        .filter(
            Loan.id == loan_id,
            Loan.finance_owner_id == finance_owner_id,
        )
        .first()
    )

    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found.",
        )

    return loan


def get_loans_by_customer(
    db: Session,
    customer_id: int,
    finance_owner_id: int,
):
    """
    Return all loans belonging to the specified customer.
    """

    return (
        db.query(Loan)
        .filter(
            Loan.customer_id == customer_id,
            Loan.finance_owner_id == finance_owner_id,
        )
        .all()
    )


def update_loan(
    db: Session,
    loan_id: int,
    loan_data: LoanUpdate,
    finance_owner_id: int,
):
    """
    Update editable loan information.
    """

    loan = (
        db.query(Loan)
        .filter(
            Loan.id == loan_id,
            Loan.finance_owner_id == finance_owner_id,
        )
        .first()
    )

    if not loan:
        return None

    loan.interest_method = loan_data.interest_method
    loan.interest_rate = loan_data.interest_rate
    loan.due_date = loan_data.due_date

    db.commit()
    db.refresh(loan)

    return loan


def search_loans(
    db: Session,
    finance_owner_id: int,
    customer_name: Optional[str] = None,
    mobile_number: Optional[str] = None,
    status_filter: Optional[str] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
):
    """
    Search loans using one or more optional filters.
    """

    query = (
        db.query(Loan)
        .join(Customer)
        .filter(
            Loan.finance_owner_id == finance_owner_id,
            Customer.finance_owner_id == finance_owner_id,
        )
    )

    if customer_name:
        query = query.filter(
            Customer.full_name.ilike(f"%{customer_name}%")
        )

    if mobile_number:
        query = query.filter(
            Customer.phone.ilike(f"%{mobile_number}%")
        )

    if status_filter:
        query = query.filter(
            Loan.status == status_filter.upper()
        )

    if from_date:
        query = query.filter(
            Loan.issue_date >= from_date
        )

    if to_date:
        query = query.filter(
            Loan.issue_date <= to_date
        )

    return (
        query.order_by(Loan.issue_date.desc())
        .all()
    )