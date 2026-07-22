from sqlalchemy.orm import Session

from backend.app.models.finance_settings import FinanceSettings
from backend.app.schemas.finance_settings import FinanceSettingsUpdate


def get_finance_settings(
    db: Session,
    finance_owner_id: int,
) -> FinanceSettings | None:
    return (
        db.query(FinanceSettings)
        .filter(
            FinanceSettings.finance_owner_id == finance_owner_id
        )
        .first()
    )


def update_finance_settings(
    db: Session,
    finance_owner_id: int,
    settings_data: FinanceSettingsUpdate,
) -> FinanceSettings:
    settings = (
        db.query(FinanceSettings)
        .filter(
            FinanceSettings.finance_owner_id == finance_owner_id
        )
        .first()
    )

    if settings is None:
        raise ValueError("Finance settings not found.")

    update_data = settings_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(settings, field, value)

    db.commit()
    db.refresh(settings)

    return settings