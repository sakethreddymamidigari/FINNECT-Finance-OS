"""
Finance Owner API

Contains endpoints for finance owner registration,
authentication, and profile management.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_finance_owner
from backend.app.database.session import get_db
from backend.app.models.finance_owner import FinanceOwner
from backend.app.schemas.finance_owner import (
    FinanceOwnerCreate,
    FinanceOwnerResponse,
    Token,
)
from backend.app.services.finance_owner_service import (
    authenticate_finance_owner,
    create_finance_owner,
)

router = APIRouter(
    prefix="/finance-owners",
    tags=["Finance Owners"],
)


@router.post(
    "/register",
    response_model=FinanceOwnerResponse,
)
def register_finance_owner(
    owner: FinanceOwnerCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new finance owner.
    """
    try:
        return create_finance_owner(db, owner)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate a finance owner and return a JWT access token.
    """

    try:
        return authenticate_finance_owner(
            db,
            form_data.username,
            form_data.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )


@router.get(
    "/me",
    response_model=FinanceOwnerResponse,
)
def get_profile(
    owner: FinanceOwner = Depends(get_current_finance_owner),
):
    """
    Return the currently authenticated finance owner's profile.
    """
    return owner