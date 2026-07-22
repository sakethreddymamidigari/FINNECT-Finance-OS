from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_finance_owner
from backend.app.database.deps import get_db
from backend.app.models.finance_owner import FinanceOwner
from backend.app.schemas.loan import LoanCreate, LoanUpdate, LoanResponse
from backend.app.services.loan_service import (
    create_loan,
    get_loans,
    get_loan_by_id,
    update_loan,
    get_loans_by_customer,
    search_loans,
    get_loans_due_this_month,
    get_loans_due_by_month,
    get_interest_summary,
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
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    return create_loan(
        db=db,
        loan=loan,
        finance_owner_id=current_owner.id,
    )


@router.get(
    "/search",
    response_model=List[LoanResponse],
    summary="Search Loans",
)
def search_loans_endpoint(
    customer_name: Optional[str] = Query(
        default=None,
        description="Filter by customer name",
    ),
    mobile_number: Optional[str] = Query(
        default=None,
        description="Filter by customer mobile number",
    ),
    status_filter: Optional[str] = Query(
        default=None,
        alias="status",
        description="Loan status (ACTIVE/CLOSED)",
    ),
    from_date: Optional[date] = Query(
        default=None,
        description="Loan start date from",
    ),
    to_date: Optional[date] = Query(
        default=None,
        description="Loan start date to",
    ),
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    """
    Search loans using optional filters.
    """

    return search_loans(
        db=db,
        finance_owner_id=current_owner.id,
        customer_name=customer_name,
        mobile_number=mobile_number,
        status_filter=status_filter,
        from_date=from_date,
        to_date=to_date,
    )


@router.get(
    "/customer/{customer_id}",
    response_model=List[LoanResponse],
)
def get_customer_loans_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    """
    Return all loans belonging to a customer.
    """

    return get_loans_by_customer(
        db=db,
        customer_id=customer_id,
        finance_owner_id=current_owner.id,
    )

@router.get(
    "/due-this-month",
    response_model=List[LoanResponse],
    summary="Get Loans Due This Month",
)
def get_loans_due_this_month_endpoint(
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    """
    Return all active loans due in the current month.
    """

    return get_loans_due_this_month(
        db=db,
        finance_owner_id=current_owner.id,
    )

@router.get(
    "/due",
    response_model=List[LoanResponse],
    summary="Get Loans Due By Month",
)
def get_loans_due_by_month_endpoint(
    month: int,
    year: int,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    """
    Return all active loans due in the specified month and year.
    """

    return get_loans_due_by_month(
        db=db,
        finance_owner_id=current_owner.id,
        month=month,
        year=year,
    )

@router.get(
    "/{loan_id}/interest-summary",
    summary="Get Loan Interest Summary",
)
def get_interest_summary_endpoint(
    loan_id: int,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    """
    Calculate the current interest for a loan without
    modifying any database values.
    """

    # Delegate the calculation to the service layer.
    # The service validates ownership and performs
    # the interest calculation.
    
    return get_interest_summary(
        db=db,
        loan_id=loan_id,
        finance_owner_id=current_owner.id,
    )

@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
)
def get_loan_by_id_endpoint(
    loan_id: int,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
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
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    return get_loans(
        db=db,
        finance_owner_id=current_owner.id,
    )


@router.put(
    "/{loan_id}",
    response_model=LoanResponse,
)
def update_existing_loan(
    loan_id: int,
    loan_data: LoanUpdate,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    """
    Update an existing loan.
    """

    loan = update_loan(
        db=db,
        loan_id=loan_id,
        loan_data=loan_data,
        finance_owner_id=current_owner.id,
    )

    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found",
        )

    return loan