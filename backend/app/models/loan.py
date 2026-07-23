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

    # Date from which interest starts accruing.
    interest_start_date = Column(
        Date,
        nullable=False,
    )

    status = Column(
        String,
        default="ACTIVE",
    )

    parent_loan_id = Column(
        Integer,
        ForeignKey("loans.id", ondelete="SET NULL"),
        nullable=True,
    )

    parent_loan = relationship(
        "Loan",
        remote_side="Loan.id",
        foreign_keys=[parent_loan_id],
        backref="child_loans",
    )

    # Settlement details (applicable only for settlement closures)
    settlement_amount = Column(Numeric(12, 2), nullable=True)
    waived_amount = Column(Numeric(12, 2), nullable=True)
    settlement_date = Column(Date, nullable=True)
    settlement_reason = Column(String(255), nullable=True)

    # Closure type: NORMAL or SETTLEMENT
    closure_type = Column(String(20), nullable=True)

    # Stores when the loan is permanently closed.
    # It remains NULL while the loan is active.
    closed_at = Column(
        DateTime,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    # Stores the last date up to which interest has been calculated.
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

    renewals = relationship(
        "LoanRenewal",
        foreign_keys="LoanRenewal.old_loan_id",
        back_populates="old_loan",
        cascade="all, delete-orphan",
    )

    payments = relationship(
        "Payment",
        back_populates="loan",
        cascade="all, delete-orphan",
    )