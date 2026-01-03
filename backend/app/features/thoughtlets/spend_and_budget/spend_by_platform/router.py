"""
Thoughtlets Spend and Budget - Spend by Platform router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import spend_by_platform_service
from .models import SpendByPlatformResponse

router = APIRouter()


@router.get(
    "/spend-by-platform",
    response_model=SpendByPlatformResponse,
    summary="Get spend breakdown by platform",
    description="Retrieve spend allocation across different advertising platforms. Optionally filter by date range."
)
async def get_spend_by_platform(
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
    Get spend breakdown by platform including:
    - Platform name
    - Spend amount per platform
    - Total spend across all platforms

    Data is aggregated from all advertising platforms (Google Ads, Meta Ads, etc.).
    """
    return spend_by_platform_service.get_spend_by_platform(
        date_from=date_from,
        date_to=date_to
    )
