"""
Create all database tables.
Run this file whenever a new model is added.
"""

from backend.app.database.base import Base
from backend.app.database.connection import engine

# Import all models
from backend.app.models.finance_owner import FinanceOwner
from backend.app.models.customer import Customer

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Done!")