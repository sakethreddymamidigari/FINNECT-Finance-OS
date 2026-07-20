from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_finance_owner
from backend.app.database.deps import get_db
from backend.app.models.finance_owner import FinanceOwner
from backend.app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
)
from backend.app.services.payment_service import (
    create_payment,
    get_payment,
    get_loan_payments,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment_endpoint(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(
        get_current_finance_owner,
    ),
):
    return create_payment(
        db=db,
        payment=payment,
        finance_owner_id=current_owner.id,
    )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def get_payment_endpoint(
    payment_id: int,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(
        get_current_finance_owner,
    ),
):
    return get_payment(
        db=db,
        payment_id=payment_id,
        finance_owner_id=current_owner.id,
    )


@router.get(
    "/loan/{loan_id}",
    response_model=List[PaymentResponse],
)
def get_loan_payments_endpoint(
    loan_id: int,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(
        get_current_finance_owner,
    ),
):
    return get_loan_payments(
        db=db,
        loan_id=loan_id,
        finance_owner_id=current_owner.id,
    )