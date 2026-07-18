from backend.app.database.base import Base
from backend.app.database.connection import engine

from backend.app.models.finance_owner import FinanceOwner
from backend.app.models.customer import Customer
from backend.app.models.loan import Loan
from backend.app.models.payment import Payment

Base.metadata.create_all(bind=engine)

print("Done!")