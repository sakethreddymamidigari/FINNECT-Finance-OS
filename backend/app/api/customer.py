from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from backend.app.database.deps import get_db
from backend.app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerListResponse,
    CustomerLedgerResponse,
)
from backend.app.services.customer_service import (
    create_customer,
    get_customers,
    get_customer_names,
    search_customers,
    get_customer_ledger,
)
from backend.app.core.auth import get_current_finance_owner
from backend.app.models.finance_owner import FinanceOwner

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer_endpoint(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    return create_customer(
        db=db,
        customer=customer,
        finance_owner_id=current_owner.id,
    )

@router.get(
    "/search",
    response_model=List[CustomerResponse],
)
def search_customers_endpoint(
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    """
    Search customers by name or phone.
    """

    return search_customers(
        db=db,
        finance_owner_id=current_owner.id,
        query=query,
    )

@router.get(
    "/",
    response_model=List[CustomerResponse],
)
def get_customers_endpoint(
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    return get_customers(
        db=db,
        finance_owner_id=current_owner.id,
    )


@router.get(
    "/names",
    response_model=List[CustomerListResponse],
)

def get_customer_names_endpoint(
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    """
    Return customer IDs and names for dropdown selection.
    """

    return get_customer_names(
        db=db,
        finance_owner_id=current_owner.id,
    )

@router.get(
    "/{customer_id}/ledger",
    response_model=CustomerLedgerResponse,
    summary="Customer Ledger",
)
def get_customer_ledger_endpoint(
    customer_id: int,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(get_current_finance_owner),
):
    """
    Return the complete ledger for the selected customer.
    """

    return get_customer_ledger(
        db=db,
        customer_id=customer_id,
        finance_owner_id=current_owner.id,
    )