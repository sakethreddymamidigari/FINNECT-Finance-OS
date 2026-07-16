"""
Authentication utilities.

Provides reusable authentication dependencies
for protected API endpoints.
"""

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.app.core.security import SECRET_KEY, ALGORITHM
from backend.app.database.session import get_db
from backend.app.models.finance_owner import FinanceOwner

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/finance-owners/login"
)


def get_current_finance_owner(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Validate the JWT token and return
    the authenticated finance owner.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        owner_id = payload.get("owner_id")

        if owner_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token."
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token."
        )

    owner = (
        db.query(FinanceOwner)
        .filter(FinanceOwner.id == owner_id)
        .first()
    )

    if owner is None:
        raise HTTPException(
            status_code=401,
            detail="Finance owner not found."
        )

    return owner