"""
GA4 Analytics Overview router - API endpoints for overview operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import ga4_overview_service
from .models import GA4OverviewResponse

router = APIRouter()


@router.get(
    "/overview",
    response_model=GA4OverviewResponse,
    summary="Get GA4 Analytics overview metrics",
    description="Retrieve aggregated GA4 Analytics performance metrics. Optionally filter by date range."
)
async def get_ga4_overview(
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
    Get GA4 Analytics overview metrics including:
    - Sessions
    - Users
    - Engaged Sessions
    - Engagement Rate
    - Sessions per User
    - Conversions
    - Revenue
    - Conversion Value
    """
    return ga4_overview_service.get_overview(
        date_from=date_from,
        date_to=date_to
    )
