"""
Monthly Conversions router - API endpoints for monthly conversion metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import monthly_conversions_service
from .models import MonthlyConversionsResponse

router = APIRouter()


@router.get(
    "/monthly-conversions",
    response_model=MonthlyConversionsResponse,
    summary="Get monthly conversions trend",
    description="Retrieve conversion volume aggregated by month. Optionally filter by date range."
)
async def get_monthly_conversions(
    date_from: Optional[date] = Query(
        default=None,
        description="Start date for metrics (YYYY-MM-DD format). If not provided, no start date filter.",
        example="2024-01-01"
    ),
    date_to: Optional[date] = Query(
        default=None,
        description="End date for metrics (YYYY-MM-DD format). If not provided, no end date filter.",
        example="2024-12-31"
    ),
):
    """
    Get monthly conversions trend data including:
    - Month label (e.g., 'Nov 2025', 'Dec 2025')
    - Conversions for each month
    - Total conversions across all months

    Data is aggregated from campaign performance metrics.
    """
    return monthly_conversions_service.get_monthly_conversions(
        date_from=date_from,
        date_to=date_to
    )
