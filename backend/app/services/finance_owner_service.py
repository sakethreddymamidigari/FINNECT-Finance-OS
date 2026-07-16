from sqlalchemy.orm import Session

from backend.app.models.finance_owner import FinanceOwner
from backend.app.schemas.finance_owner import FinanceOwnerCreate
from backend.app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)


def create_finance_owner(
    db: Session,
    owner: FinanceOwnerCreate
):
    existing_owner = (
        db.query(FinanceOwner)
        .filter(
            (FinanceOwner.email == owner.email) |
            (FinanceOwner.phone == owner.phone)
        )
        .first()
    )

    if existing_owner:
        raise ValueError(
            "Finance owner already exists."
        )

    db_owner = FinanceOwner(
        business_name=owner.business_name,
        owner_name=owner.owner_name,
        phone=owner.phone,
        email=owner.email,
        password_hash=hash_password(owner.password),
        address=owner.address
    )

    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)

    return db_owner

def login_finance_owner(
    db: Session,
    email: str,
    password: str
):
    owner = (
        db.query(FinanceOwner)
        .filter(FinanceOwner.email == email)
        .first()
    )

    if owner is None:
        raise ValueError("Invalid email or password")

    if not verify_password(
        password,
        owner.password_hash
    ):
        raise ValueError("Invalid email or password")

    token = create_access_token(
        {
            "sub": owner.email,
            "owner_id": owner.id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }