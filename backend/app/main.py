from fastapi import FastAPI

from backend.app.api.finance_owner import router as finance_owner_router
from backend.app.api.customer import router as customer_router

app = FastAPI(
    title="FINNECT Finance OS",
    version="1.0.0",
    description="Digital operating system for local finance businesses."
)

app.include_router(finance_owner_router)
app.include_router(customer_router)

@app.get("/")
def root():
    return {
        "project": "FINNECT Finance OS",
        "status": "Running"
    }