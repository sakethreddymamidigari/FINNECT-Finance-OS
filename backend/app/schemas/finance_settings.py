from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class FinanceSettingsBase(BaseModel):
    business_name: Optional[str] = Field(None, max_length=150)
    owner_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, max_length=300)

    default_interest_method: str
    default_interest_rate: Decimal
    default_loan_duration: int
    default_grace_period: int

    currency: str
    date_format: str
    timezone: str

    maturity_alert_days: int


class FinanceSettingsUpdate(FinanceSettingsBase):
    pass


class FinanceSettingsResponse(FinanceSettingsBase):
    id: int
    finance_owner_id: int

    model_config = ConfigDict(from_attributes=True)