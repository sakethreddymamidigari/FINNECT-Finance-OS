from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.app.models.customer import Customer
from backend.app.schemas.customer import (
    CustomerCreate,
    CustomerLedgerPaymentResponse,
    CustomerLedgerLoanResponse,
    CustomerLedgerSummaryResponse,
    CustomerLedgerResponse,
)

from backend.app.models.loan import Loan
from backend.app.models.payment import Payment
from backend.app.utils.interest_calculator import calculate_interest

from decimal import Decimal
from datetime import date


def create_customer(
    db: Session,
    customer: CustomerCreate,
    finance_owner_id: int,
) -> Customer:
    """
    Create a new customer for the authenticated finance owner.
    """

    db_customer = Customer(
        full_name=customer.full_name,
        phone=customer.phone,
        address=customer.address,
        finance_owner_id=finance_owner_id,
    )

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


def get_customers(
    db: Session,
    finance_owner_id: int,
):
    """
    Return all customers belonging to the authenticated finance owner.
    """

    return (
        db.query(Customer)
        .filter(Customer.finance_owner_id == finance_owner_id)
        .all()
    )


def get_customer_names(
    db: Session,
    finance_owner_id: int,
):
    """
    Return only customer IDs and names for dropdown selection.
    """

    return (
        db.query(Customer.id, Customer.full_name)
        .filter(Customer.finance_owner_id == finance_owner_id)
        .order_by(Customer.full_name)
        .all()
    )

def search_customers(
    db: Session,
    finance_owner_id: int,
    query: str,
):
    """
    Search customers by name or phone.
    """

    return (
        db.query(Customer)
        .filter(
            Customer.finance_owner_id == finance_owner_id,
            or_(
                Customer.full_name.ilike(f"%{query}%"),
                Customer.phone.ilike(f"%{query}%"),
            ),
        )
        .order_by(Customer.full_name)
        .all()
    )

def get_customer_ledger(
    db: Session,
    customer_id: int,
    finance_owner_id: int,
):
    """
    Return the complete ledger for a customer.
    """

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id,
            Customer.finance_owner_id == finance_owner_id,
        )
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found.",
        )

    loans = (
        db.query(Loan)
        .filter(
            Loan.customer_id == customer.id,
            Loan.finance_owner_id == finance_owner_id,
        )
        .order_by(Loan.issue_date.desc())
        .all()
    )

    ledger_loans = []

    total_principal = Decimal("0.00")
    remaining_principal = Decimal("0.00")
    total_interest_paid = Decimal("0.00")
    accrued_interest = Decimal("0.00")

    active_loans = 0
    closed_loans = 0

    today = date.today()

    for loan in loans:

        if loan.status == "ACTIVE":
            active_loans += 1
        else:
            closed_loans += 1

        total_principal += loan.principal_amount
        remaining_principal += loan.remaining_principal
        total_interest_paid += loan.total_interest_paid

        current_interest = calculate_interest(
            principal=loan.remaining_principal,
            rate=loan.interest_rate,
            method=loan.interest_method,
            start_date=loan.last_interest_calculated_on,
            end_date=today,
        )

        accrued_interest += current_interest

        payments = (
            db.query(Payment)
            .filter(
                Payment.loan_id == loan.id,
                Payment.finance_owner_id == finance_owner_id,
            )
            .order_by(Payment.payment_date.desc())
            .all()
        )

        ledger_payments = []

        for payment in payments:
            ledger_payments.append(
                CustomerLedgerPaymentResponse(
                    payment_date=payment.payment_date,
                    amount_paid=payment.amount_paid,
                    principal_paid=payment.principal_paid,
                    interest_paid=payment.interest_paid,
                    payment_mode=payment.payment_mode,
                    remarks=payment.remarks,
                )
            )

        ledger_loans.append(
            CustomerLedgerLoanResponse(
                loan_id=loan.id,
                principal_amount=loan.principal_amount,
                remaining_principal=loan.remaining_principal,
                total_principal_paid=loan.total_principal_paid,
                total_interest_paid=loan.total_interest_paid,
                accrued_interest=current_interest,
                total_outstanding=loan.remaining_principal + current_interest,
                issue_date=loan.issue_date,
                due_date=loan.due_date,
                status=loan.status,
                payments=ledger_payments,
            )
        )

    return CustomerLedgerResponse(
        customer=customer,
        summary=CustomerLedgerSummaryResponse(
            total_loans=len(loans),
            active_loans=active_loans,
            closed_loans=closed_loans,
            total_principal=total_principal,
            remaining_principal=remaining_principal,
            total_interest_paid=total_interest_paid,
            accrued_interest=accrued_interest,
            total_outstanding=remaining_principal + accrued_interest,
        ),
        loans=ledger_loans,
    )