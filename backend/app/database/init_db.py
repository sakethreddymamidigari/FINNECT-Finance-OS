from backend.app.database.base import Base
from backend.app.database.connection import engine

#import all models
from backend.app.models.finance_owner import FinanceOwner

print("Creating database table...")

Base.metadata.create_all(bind=engine)

print("Done!")