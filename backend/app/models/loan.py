from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.app.database.base import Base


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    finance_owner_id = Column(
        Integer,
        ForeignKey("finance_owners.id"),
        nullable=False,
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
    )

    principal_amount = Column(
        Numeric(12, 2),
        nullable=False,
    )

    remaining_principal = Column(
        Numeric(12, 2),
        nullable=False,
    )

    total_principal_paid = Column(
        Numeric(12, 2),
        default=0,
    )

    total_interest_paid = Column(
        Numeric(12, 2),
        default=0,
    )

    interest_method = Column(
        String,
        nullable=False,
    )

    interest_rate = Column(
        Numeric(10, 2),
        nullable=False,
    )

    issue_date = Column(
        Date,
        nullable=False,
    )

    due_date = Column(
        Date,
        nullable=False,
    )

    # NEW FIELD
    interest_start_date = Column(
        Date,
        nullable=False,
    )

    status = Column(
        String,
        default="ACTIVE",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    last_interest_calculated_on = Column(
        Date,
        nullable=True,
    )

    finance_owner = relationship(
        "FinanceOwner",
        back_populates="loans",
    )

    customer = relationship(
        "Customer",
        back_populates="loans",
    )

    payments = relationship(
        "Payment",
        back_populates="loan",
        cascade="all, delete-orphan",
    )