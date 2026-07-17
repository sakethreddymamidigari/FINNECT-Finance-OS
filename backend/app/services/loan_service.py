from fastapi import HTTPException, status

from backend.app.models.customer import Customer

from sqlalchemy.orm import Session

from backend.app.models.loan import Loan
from backend.app.schemas.loan import LoanCreate


def create_loan(
    db: Session,
    loan: LoanCreate,
    finance_owner_id: int,
):
    """
    Create a loan only if the customer belongs
    to the authenticated finance owner.
    """

    remaining_principal=loan.principal_amount,

    total_principal_paid=0,

    total_interest_paid=0,

    last_interest_calculated_on=loan.issue_date,

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
        interest_method=loan.interest_method,
        interest_rate=loan.interest_rate,
        issue_date=loan.issue_date,
        due_date=loan.due_date,
    )

    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)

    return db_loan

def get_loans(
    db: Session,
    finance_owner_id: int,
):
    """
    Return all loans belonging to the authenticated finance owner.
    """

    return (
        db.query(Loan)
        .filter(
            Loan.finance_owner_id == finance_owner_id
        )
        .all()
    )