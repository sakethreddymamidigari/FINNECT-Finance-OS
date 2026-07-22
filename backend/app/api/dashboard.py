"""
Dashboard API routes.

Provides consolidated dashboard statistics for the authenticated
finance owner.
"""

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_finance_owner
from backend.app.database.deps import get_db
from backend.app.models.finance_owner import FinanceOwner
from backend.app.schemas.dashboard import (
    DashboardResponse,
    ProfitSummaryResponse,
    MaturityReportResponse,
)
from backend.app.services.dashboard_service import (
    get_dashboard,
    get_profit_summary,
    get_maturity_report,
)

# --------------------------------------------------
# Dashboard Router
# --------------------------------------------------

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# --------------------------------------------------
# Dashboard Endpoint
# --------------------------------------------------

@router.get(
    "",
    response_model=DashboardResponse,
)
def get_dashboard_endpoint(
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(
        get_current_finance_owner,
    ),
):
    """
    Return dashboard statistics for the logged-in finance owner.
    """

    return get_dashboard(
        db=db,
        finance_owner_id=current_owner.id,
    )
@router.get(
    "/profit-summary",
    response_model=ProfitSummaryResponse,
)
def get_profit_summary_endpoint(
    from_date: date = Query(...),
    to_date: date = Query(...),
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(
        get_current_finance_owner,
    ),
):
    """
    Return profit summary for the selected date range.
    """

    return get_profit_summary(
        db=db,
        finance_owner_id=current_owner.id,
        from_date=from_date,
        to_date=to_date,
    )

@router.get(
    "/maturity-report",
    response_model=MaturityReportResponse,
)
def get_maturity_report_endpoint(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000),
    db: Session = Depends(get_db),
    current_owner: FinanceOwner = Depends(
        get_current_finance_owner,
    ),
):
    """
    Return all loans maturing in the selected month and year.
    """

    return get_maturity_report(
        db=db,
        finance_owner_id=current_owner.id,
        month=month,
        year=year,
    )