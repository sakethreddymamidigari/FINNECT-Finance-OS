from sqlalchemy import Column, Integer, String
from backend.app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    address = Column(String(255))