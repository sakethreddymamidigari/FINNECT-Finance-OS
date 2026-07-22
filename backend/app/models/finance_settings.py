from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.database.base import Base


class FinanceSettings(Base):
    __tablename__ = "finance_settings"

    id = Column(Integer, primary_key=True, index=True)

    finance_owner_id = Column(
        Integer,
        ForeignKey("finance_owners.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    business_name = Column(String(150), nullable=True)
    owner_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(120), nullable=True)
    address = Column(String(300), nullable=True)

    default_interest_method = Column(
        String(20),
        nullable=False,
        default="PERCENTAGE",
    )

    default_interest_rate = Column(
        Numeric(10, 2),
        nullable=False,
        default=5.00,
    )

    default_loan_duration = Column(
        Integer,
        nullable=False,
        default=12,
    )

    default_grace_period = Column(
        Integer,
        nullable=False,
        default=0,
    )

    currency = Column(
        String(10),
        nullable=False,
        default="INR",
    )

    date_format = Column(
        String(20),
        nullable=False,
        default="DD/MM/YYYY",
    )

    timezone = Column(
        String(50),
        nullable=False,
        default="Asia/Kolkata",
    )

    maturity_alert_days = Column(
        Integer,
        nullable=False,
        default=30,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    finance_owner = relationship(
        "FinanceOwner",
        back_populates="settings",
    )