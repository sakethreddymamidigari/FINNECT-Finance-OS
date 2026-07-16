from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.session import get_db
from backend.app.schemas.finance_owner import (
    FinanceOwnerCreate,
    FinanceOwnerResponse,
    FinanceOwnerLogin,
    Token
)
from backend.app.services.finance_owner_service import (
    create_finance_owner,
    login_finance_owner
)

router = APIRouter(
    prefix="/finance-owners",
    tags=["Finance Owners"]
)


@router.post("/register",response_model= FinanceOwnerResponse)
def register_finance_owner(
    owner: FinanceOwnerCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_finance_owner(db, owner)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
@router.post(
    "/login",
    response_model=Token
)
def login(
    credentials: FinanceOwnerLogin,
    db: Session = Depends(get_db)
):
    try:
        return login_finance_owner(
            db,
            credentials.email,
            credentials.password
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )