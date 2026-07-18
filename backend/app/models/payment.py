from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Date,
    DateTime,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.database.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    finance_owner_id = Column(
        Integer,
        ForeignKey("finance_owners.id"),
        nullable=False,
    )

    loan_id = Column(
        Integer,
        ForeignKey("loans.id"),
        nullable=False,
    )

    payment_date = Column(
        Date,
        nullable=False,
    )

    amount_paid = Column(
        Numeric(12, 2),
        nullable=False,
    )

    interest_paid = Column(
        Numeric(12, 2),
        nullable=False,
    )

    principal_paid = Column(
        Numeric(12, 2),
        nullable=False,
    )

    payment_mode = Column(
        String(50),
        nullable=False,
    )

    remarks = Column(
        String(255),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    finance_owner = relationship(
        "FinanceOwner",
        back_populates="payments",
    )

    loan = relationship(
        "Loan",
        back_populates="payments",
    )