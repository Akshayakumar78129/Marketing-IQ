"""
Meta Ads Daily Performance router - API endpoints for daily metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import meta_ads_daily_performance_service
from .models import MetaAdsDailyPerformanceListResponse

router = APIRouter()


@router.get(
    "/daily-performance",
    response_model=MetaAdsDailyPerformanceListResponse,
    summary="Get Meta Ads daily performance",
    description="Retrieve daily Meta Ads performance metrics. Optionally filter by date range and campaign."
)
async def get_meta_ads_daily_performance(
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
    campaign_id: Optional[str] = Query(
        default=None,
        description="Filter by specific campaign ID",
        example="120237636434930286"
    ),
):
    """
    Get Meta Ads daily performance metrics including:
    - Date
    - Daily Spend
    - Impressions
    - Clicks
    - Conversions
    - Revenue
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    """
    return meta_ads_daily_performance_service.get_daily_performance(
        date_from=date_from,
        date_to=date_to,
        campaign_id=campaign_id
    )
