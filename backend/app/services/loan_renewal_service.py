from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.app.models.loan import Loan
from backend.app.models.loan_renewal import LoanRenewal
from backend.app.schemas.loan_renewal import LoanRenewalCreate
from backend.app.utils.interest_calculator import calculate_interest


def renew_loan(
    db: Session,
    loan_id: int,
    finance_owner_id: int,
    renewal: LoanRenewalCreate,
):
    # Retrieve the loan and ensure it belongs to the authenticated finance owner.
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

    # Only active loans are eligible for renewal.
    if loan.status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only active loans can be renewed.",
        )

    # Use a single date reference throughout the transaction.
    today = date.today()

    # Normalize the interest method before saving it.
    interest_method = renewal.interest_method.strip().upper()

    # Calculate the outstanding interest from the last calculation date.
    accrued_interest = calculate_interest(
        principal=loan.remaining_principal,
        rate=loan.interest_rate,
        method=loan.interest_method,
        start_date=loan.last_interest_calculated_on,
        end_date=today,
    )

    if renewal.renewal_type == "CONTINUE":

        # Record the renewal while continuing with the same loan.
        history = LoanRenewal(
            old_loan_id=loan.id,
            new_loan_id=loan.id,
            finance_owner_id=finance_owner_id,
            renewal_type="CONTINUE",
            old_due_date=loan.due_date,
            new_due_date=renewal.new_due_date,
            old_interest_method=loan.interest_method,
            new_interest_method=interest_method,
            old_interest_rate=loan.interest_rate,
            new_interest_rate=renewal.interest_rate,
            remaining_principal=loan.remaining_principal,
            outstanding_interest=accrued_interest,
            new_principal=loan.remaining_principal,
            remarks=renewal.remarks,
        )

        # Apply the renewed terms to the existing loan.
        loan.due_date = renewal.new_due_date
        loan.interest_method = interest_method
        loan.interest_rate = renewal.interest_rate
        loan.last_interest_calculated_on = today

        db.add(history)

    else:

        # Add the outstanding interest to the remaining principal.
        new_principal = (
            loan.remaining_principal
            + accrued_interest
        )

        # Preserve the original loan for audit purposes.
        loan.status = "RENEWED"

        # Create a fresh loan that represents the renewed agreement.
        new_loan = Loan(
            customer_id=loan.customer_id,
            finance_owner_id=loan.finance_owner_id,
            parent_loan_id=loan.id,
            principal_amount=new_principal,
            remaining_principal=new_principal,
            total_principal_paid=0,
            total_interest_paid=0,
            interest_method=interest_method,
            interest_rate=renewal.interest_rate,
            issue_date=today,
            interest_start_date=today,
            last_interest_calculated_on=today,
            due_date=renewal.new_due_date,
            status="ACTIVE",
        )

        db.add(new_loan)

        # Flush so SQLAlchemy generates the new loan ID.
        db.flush()

        # Refresh to populate all generated values.
        db.refresh(new_loan)

        # Store the renewal history linking the old and new loans.
        history = LoanRenewal(
            old_loan_id=loan.id,
            new_loan_id=new_loan.id,
            finance_owner_id=finance_owner_id,
            renewal_type="CAPITALIZE",
            old_due_date=loan.due_date,
            new_due_date=renewal.new_due_date,
            old_interest_method=loan.interest_method,
            new_interest_method=interest_method,
            old_interest_rate=loan.interest_rate,
            new_interest_rate=renewal.interest_rate,
            remaining_principal=loan.remaining_principal,
            outstanding_interest=accrued_interest,
            new_principal=new_principal,
            remarks=renewal.remarks,
        )

        db.add(history)

    # Persist all changes in a single transaction.
    db.commit()

    # Reload the renewal history so generated values are available.
    db.refresh(history)

    return history


def get_loan_renewals(
    db: Session,
    loan_id: int,
    finance_owner_id: int,
):
    # Return all renewals for the specified loan in descending order.
    return (
        db.query(LoanRenewal)
        .filter(
            LoanRenewal.old_loan_id == loan_id,
            LoanRenewal.finance_owner_id == finance_owner_id,
        )
        .order_by(LoanRenewal.renewed_at.desc())
        .all()
    )