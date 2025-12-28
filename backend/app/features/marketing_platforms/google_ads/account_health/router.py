"""
Google Ads Account Health router - API endpoints for account health operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import account_health_service
from .models import AccountHealthResponse

router = APIRouter()


@router.get(
    "/account-health",
    response_model=AccountHealthResponse,
    summary="Get Google Ads account health",
    description="Retrieve Google Ads account health metrics with optional date range filters for ROAS calculation."
)
async def get_account_health(
    date_from: Optional[date] = Query(
        default=None,
        description="Start date for ROAS calculation (YYYY-MM-DD format). If not provided, no start date filter.",
        example="2024-01-01"
    ),
    date_to: Optional[date] = Query(
        default=None,
        description="End date for ROAS calculation (YYYY-MM-DD format). If not provided, no end date filter.",
        example="2024-12-31"
    ),
):
    """
    Get Google Ads account health metrics including:
    - Total Campaigns
    - Active Campaigns (enabled)
    - Average ROAS (Return on Ad Spend)
    - Total Keywords
    """
    return account_health_service.get_account_health(
        date_from=date_from,
        date_to=date_to
    )
