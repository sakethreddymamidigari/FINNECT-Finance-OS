from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.database.deps import get_db
from backend.app.schemas.customer import CustomerCreate, CustomerResponse
from backend.app.services.customer_service import (
    create_customer,
    get_customers,
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