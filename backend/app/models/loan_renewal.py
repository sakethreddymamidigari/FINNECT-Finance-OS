from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Date,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.database.base import Base


class LoanRenewal(Base):
    __tablename__ = "loan_renewals"

    id = Column(Integer, primary_key=True, index=True)

    old_loan_id = Column(
        Integer,
        ForeignKey("loans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    new_loan_id = Column(
        Integer,
        ForeignKey("loans.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    finance_owner_id = Column(
        Integer,
        ForeignKey("finance_owners.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    renewal_type = Column(
        String(20),
        nullable=False,
    )

    old_due_date = Column(
        Date,
        nullable=False,
    )

    new_due_date = Column(
        Date,
        nullable=False,
    )

    old_interest_method = Column(
        String(20),
        nullable=False,
    )

    new_interest_method = Column(
        String(20),
        nullable=False,
    )

    old_interest_rate = Column(
        Numeric(10, 2),
        nullable=False,
    )

    new_interest_rate = Column(
        Numeric(10, 2),
        nullable=False,
    )

    remaining_principal = Column(
        Numeric(12, 2),
        nullable=False,
    )

    outstanding_interest = Column(
        Numeric(12, 2),
        nullable=False,
    )

    new_principal = Column(
        Numeric(12, 2),
        nullable=False,
    )

    remarks = Column(
        String(255),
        nullable=True,
    )

    renewed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    old_loan = relationship(
        "Loan",
        foreign_keys=[old_loan_id],
        back_populates="renewals",
    )

    new_loan = relationship(
        "Loan",
        foreign_keys=[new_loan_id],
    )

    finance_owner = relationship(
        "FinanceOwner",
    )