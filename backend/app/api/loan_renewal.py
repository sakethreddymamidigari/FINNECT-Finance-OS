from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_finance_owner
from backend.app.database.session import get_db
from backend.app.models.finance_owner import FinanceOwner
from backend.app.schemas.loan_renewal import (
    LoanRenewalCreate,
    LoanRenewalResponse,
)
from backend.app.services.loan_renewal_service import (
    renew_loan,
    get_loan_renewals,
)

router = APIRouter(
    prefix="/loan",
    tags=["Loan Renewals"],
)


@router.post(
    "/{loan_id}/renew",
    response_model=LoanRenewalResponse,
    status_code=status.HTTP_201_CREATED,
)
def renew_existing_loan(
    loan_id: int,
    renewal: LoanRenewalCreate,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    # Create a new renewal for the specified loan.
    return renew_loan(
        db=db,
        loan_id=loan_id,
        finance_owner_id=current_owner.id,
        renewal=renewal,
    )


@router.get(
    "/{loan_id}/renewals",
    response_model=list[LoanRenewalResponse],
)
def fetch_loan_renewals(
    loan_id: int,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    # Return the complete renewal history of the loan.
    return get_loan_renewals(
        db=db,
        loan_id=loan_id,
        finance_owner_id=current_owner.id,
    )