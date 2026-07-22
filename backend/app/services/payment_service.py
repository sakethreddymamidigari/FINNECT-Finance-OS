from datetime import datetime, date
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.app.models.loan import Loan
from backend.app.models.payment import Payment
from backend.app.schemas.payment import PaymentCreate
from backend.app.utils.interest_calculator import calculate_interest


def create_payment(
    db: Session,
    payment: PaymentCreate,
    finance_owner_id: int,
):
    loan = (
        db.query(Loan)
        .filter(
            Loan.id == payment.loan_id,
            Loan.finance_owner_id == finance_owner_id,
        )
        .first()
    )

    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found.",
        )

    if loan.status == "CLOSED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan is already closed.",
        )

    amount = Decimal(payment.amount_paid)

    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment amount must be greater than zero.",
        )

    interest_due = calculate_interest(
        principal=loan.remaining_principal,
        rate=loan.interest_rate,
        method=loan.interest_method,
        start_date=loan.last_interest_calculated_on,
        end_date=payment.payment_date,
    )

    interest_paid = min(amount, interest_due)
    principal_paid = amount - interest_paid

    if principal_paid > loan.remaining_principal:
        principal_paid = loan.remaining_principal

    loan.remaining_principal -= principal_paid
    loan.total_principal_paid += principal_paid
    loan.total_interest_paid += interest_paid
    loan.last_interest_calculated_on = payment.payment_date

    if loan.remaining_principal <= Decimal("0.00"):
        loan.remaining_principal = Decimal("0.00")
        loan.status = "CLOSED"
        loan.closed_at = datetime.utcnow()

    db_payment = Payment(
        finance_owner_id=finance_owner_id,
        loan_id=loan.id,
        payment_date=payment.payment_date,
        amount_paid=payment.amount_paid,
        interest_paid=interest_paid,
        principal_paid=principal_paid,
        payment_mode=payment.payment_mode,
        remarks=payment.remarks,
    )

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return db_payment


def get_payment(
    db: Session,
    payment_id: int,
    finance_owner_id: int,
):
    payment = (
        db.query(Payment)
        .filter(
            Payment.id == payment_id,
            Payment.finance_owner_id == finance_owner_id,
        )
        .first()
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found.",
        )

    return payment


def get_loan_payments(
    db: Session,
    loan_id: int,
    finance_owner_id: int,
):
    return (
        db.query(Payment)
        .filter(
            Payment.loan_id == loan_id,
            Payment.finance_owner_id == finance_owner_id,
        )
        .order_by(Payment.payment_date.desc())
        .all()
    )


def delete_payment(
    db: Session,
    payment_id: int,
    finance_owner_id: int,
):
    """
    Delete a payment and restore the loan balances.
    """

    payment = (
        db.query(Payment)
        .filter(
            Payment.id == payment_id,
            Payment.finance_owner_id == finance_owner_id,
        )
        .first()
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found.",
        )

    loan = (
        db.query(Loan)
        .filter(
            Loan.id == payment.loan_id,
            Loan.finance_owner_id == finance_owner_id,
        )
        .first()
    )

    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found.",
        )
    
    # Get the latest payment for this loan
    latest_payment = (
        db.query(Payment)
        .filter(
            Payment.loan_id == payment.loan_id,
            Payment.finance_owner_id == finance_owner_id,
        )
        .order_by(Payment.payment_date.desc(), Payment.id.desc())
        .first()
    )

    # Allow deletion only for the latest payment
    if latest_payment.id != payment.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only the latest payment can be deleted.",
        )

    # Restore loan values
    loan.remaining_principal += payment.principal_paid
    loan.total_principal_paid -= payment.principal_paid
    loan.total_interest_paid -= payment.interest_paid

    # Restore interest calculation date
    previous_payment = (
        db.query(Payment)
        .filter(
            Payment.loan_id == loan.id,
            Payment.finance_owner_id == finance_owner_id,
            Payment.payment_date < payment.payment_date,
        )
        .order_by(Payment.payment_date.desc())
        .first()
    )

    if previous_payment:
        loan.last_interest_calculated_on = previous_payment.payment_date
    else:
        loan.last_interest_calculated_on = loan.start_date

    # Reopen loan if necessary
    # Reopen the loan if the latest payment is deleted.
    if loan.status == "CLOSED":
        loan.status = "ACTIVE"
        loan.closed_at = None

    db.delete(payment)
    db.commit()

    return {
        "message": "Payment deleted successfully"
    }