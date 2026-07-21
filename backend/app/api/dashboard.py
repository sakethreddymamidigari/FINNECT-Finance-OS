"""
Dashboard API routes.

Provides consolidated dashboard statistics for the authenticated
finance owner.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.auth import get_current_finance_owner
from backend.app.database.deps import get_db
from backend.app.models.finance_owner import FinanceOwner
from backend.app.schemas.dashboard import DashboardResponse
from backend.app.services.dashboard_service import get_dashboard

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