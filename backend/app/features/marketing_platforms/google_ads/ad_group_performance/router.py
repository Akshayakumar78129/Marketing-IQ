"""
Google Ads Ad Group Performance router - API endpoints for ad group performance operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import ad_group_performance_service
from .models import AdGroupPerformanceResponse

router = APIRouter()


@router.get(
    "/ad-group-performance",
    response_model=AdGroupPerformanceResponse,
    summary="Get Google Ads ad group performance",
    description="Retrieve Google Ads ad group performance metrics with optional date range filters."
)
async def get_ad_group_performance(
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
    Get Google Ads ad group performance metrics including:
    - Ad Group Name
    - Campaign Name
    - Impressions
    - Clicks
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    - Conversions
    - CVR (Conversion Rate)
    """
    return ad_group_performance_service.get_ad_group_performance(
        date_from=date_from,
        date_to=date_to
    )
