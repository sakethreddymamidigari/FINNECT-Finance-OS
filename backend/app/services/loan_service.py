from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal

from backend.app.models.customer import Customer
from backend.app.models.loan import Loan
from backend.app.schemas.loan import LoanCreate
from backend.app.schemas.loan import LoanUpdate


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
    Return all loans of a customer belonging to the authenticated finance owner.
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
    Update editable loan details.
    Only due date, interest method and interest rate
    can be modified.
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