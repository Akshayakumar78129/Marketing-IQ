"""
Meta Ads Overview router - API endpoints for overview operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import meta_ads_overview_service
from .models import MetaAdsOverviewResponse

router = APIRouter()


@router.get(
    "/overview",
    response_model=MetaAdsOverviewResponse,
    summary="Get Meta Ads overview metrics",
    description="Retrieve aggregated Meta Ads performance metrics. Optionally filter by date range."
)
async def get_meta_ads_overview(
    date_from: Optional[date] = Query(
        default=None,
        description="Start date for metrics (YYYY-MM-DD format). If not provided, no start date filter.",
        example="2025-11-15"
    ),
    date_to: Optional[date] = Query(
        default=None,
        description="End date for metrics (YYYY-MM-DD format). If not provided, no end date filter.",
        example="2025-12-15"
    ),
):
    """
    Get Meta Ads overview metrics including:
    - Total Spend
    - Impressions
    - Reach
    - Clicks
    - Conversions
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    - CPM (Cost Per Mille)
    - ROAS (Return on Ad Spend)
    """
    return meta_ads_overview_service.get_overview(
        date_from=date_from,
        date_to=date_to
    )
