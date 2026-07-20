from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_finance_owner
from backend.app.database.deps import get_db
from backend.app.models.finance_owner import FinanceOwner
from backend.app.schemas.loan import LoanCreate, LoanResponse
from backend.app.services.loan_service import (
    create_loan,
    get_loans,
    get_loan_by_id,
)

router = APIRouter(
    prefix="/loans",
    tags=["Loans"],
)


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_loan_endpoint(
    loan: LoanCreate,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(
        get_current_finance_owner
    ),
):
    return create_loan(
        db=db,
        loan=loan,
        finance_owner_id=current_owner.id,
    )

@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
)
def get_loan_by_id_endpoint(
    loan_id: int,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(
        get_current_finance_owner
    ),
):
    return get_loan_by_id(
        db=db,
        loan_id=loan_id,
        finance_owner_id=current_owner.id,
    )

@router.get(
    "/",
    response_model=List[LoanResponse],
)
def get_loans_endpoint(
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(
        get_current_finance_owner
    ),
):
    return get_loans(
        db=db,
        finance_owner_id=current_owner.id,
    )