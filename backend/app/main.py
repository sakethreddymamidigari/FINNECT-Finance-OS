"""
FINNECT Finance OS
Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------
# API Routers
# -----------------------------
from backend.app.api.finance_owner import router as finance_owner_router
from backend.app.api.customer import router as customer_router
from backend.app.api.loan import router as loan_router
from backend.app.api.payment import router as payment_router
from backend.app.api.dashboard import router as dashboard_router
from backend.app.api.finance_settings import router as finance_settings_router
from backend.app.api.loan_renewal import router as loan_renewal_router

# -----------------------------
# FastAPI Application
# -----------------------------
app = FastAPI(
    title="FINNECT Finance OS",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Register API Routers
# -----------------------------
app.include_router(finance_owner_router)
app.include_router(customer_router)
app.include_router(loan_router)
app.include_router(payment_router)
app.include_router(dashboard_router)
app.include_router(finance_settings_router)
app.include_router(loan_renewal_router)

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    """
    Health check endpoint.
    """

    return {
        "message": "Welcome to FINNECT Finance OS API"
    }