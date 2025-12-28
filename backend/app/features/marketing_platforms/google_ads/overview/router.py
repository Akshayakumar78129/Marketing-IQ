"""
Google Ads Overview router - API endpoints for overview operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import google_ads_overview_service
from .models import GoogleAdsOverviewResponse

router = APIRouter()


@router.get(
    "/overview",
    response_model=GoogleAdsOverviewResponse,
    summary="Get Google Ads overview metrics",
    description="Retrieve aggregated Google Ads performance metrics. Optionally filter by date range."
)
async def get_google_ads_overview(
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
    Get Google Ads overview metrics including:
    - Total Spend
    - Total Conversions
    - Total Revenue
    - ROAS (Return on Ad Spend)
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    - Average Quality Score
    """
    return google_ads_overview_service.get_overview(
        date_from=date_from,
        date_to=date_to
    )
