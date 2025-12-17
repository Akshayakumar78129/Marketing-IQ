"""
Meta Ads Ad Sets router - API endpoints for ad set metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import meta_ads_ad_set_service
from .models import MetaAdsAdSetListResponse

router = APIRouter()


@router.get(
    "/ad-sets",
    response_model=MetaAdsAdSetListResponse,
    summary="Get Meta Ads ad set metrics",
    description="Retrieve Meta Ads metrics grouped by ad set. Optionally filter by date range and ad set ID."
)
async def get_meta_ads_ad_sets(
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
    ad_set_id: Optional[str] = Query(
        default=None,
        description="Filter by specific ad set ID",
        example="120211234567890"
    ),
):
    """
    Get Meta Ads ad set metrics including:
    - Ad Set ID
    - Campaign ID
    - Spend
    - Impressions
    - Clicks
    - Conversions
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    """
    return meta_ads_ad_set_service.get_ad_sets(
        date_from=date_from,
        date_to=date_to,
        ad_set_id=ad_set_id
    )
