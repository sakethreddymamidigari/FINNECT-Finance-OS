from sqlalchemy import Column, Integer, String
from backend.app.database.base import Base


class FinanceOwner(Base):
    __tablename__ = "finance_owners"

    id = Column(Integer, primary_key=True, index=True)

    business_name = Column(String(150), nullable=False)

    owner_name = Column(String(100), nullable=False)

    phone = Column(String(15), unique=True, nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    address = Column(String(255), nullable=False)