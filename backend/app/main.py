from fastapi import FastAPI

from backend.app.api.finance_owner import router as finance_owner_router
from backend.app.api.customer import router as customer_router
from backend.app.api.loan import router as loan_router
from backend.app.api.payment import router as payment_router

app = FastAPI(title="FINNECT Finance OS")


app.include_router(finance_owner_router)
app.include_router(customer_router)
app.include_router(loan_router)
app.include_router(payment_router)