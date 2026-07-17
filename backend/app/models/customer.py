from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.database.base import Base


class Customer(Base):
    """
    Stores customer details belonging to a finance owner.
    """

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    finance_owner_id = Column(
        Integer,
        ForeignKey("finance_owners.id"),
        nullable=False
    )

    full_name = Column(String(100), nullable=False)

    phone = Column(
        String(15),
        unique=True,
        nullable=False
    )

    address = Column(String(255))

    finance_owner = relationship(
        "FinanceOwner",
        back_populates="customers"
    )

    loans = relationship(
        "Loan",
        back_populates="customer",
        cascade="all, delete-orphan",
    )