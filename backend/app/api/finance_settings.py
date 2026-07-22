from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_finance_owner
from backend.app.database.session import get_db
from backend.app.models.finance_owner import FinanceOwner
from backend.app.schemas.finance_settings import (
    FinanceSettingsResponse,
    FinanceSettingsUpdate,
)
from backend.app.services.finance_settings_service import (
    get_finance_settings,
    update_finance_settings,
)

router = APIRouter(
    prefix="/settings",
    tags=["Finance Settings"],
)


@router.get(
    "/",
    response_model=FinanceSettingsResponse,
    summary="Get Finance Settings",
)
def get_settings(
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(
        get_current_finance_owner,
    ),
):
    return get_finance_settings(
        db=db,
        finance_owner_id=current_owner.id,
    )


@router.put(
    "/",
    response_model=FinanceSettingsResponse,
    summary="Update Finance Settings",
)
def update_settings(
    settings: FinanceSettingsUpdate,
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(
        get_current_finance_owner,
    ),
):
    return update_finance_settings(
        db=db,
        finance_owner_id=current_owner.id,
        settings_data=settings,
    )