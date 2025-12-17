"""
Meta Ads Ad Creatives router - API endpoints for ad creative metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import meta_ads_creative_service
from .models import MetaAdsCreativeListResponse

router = APIRouter()


@router.get(
    "/ad-creatives",
    response_model=MetaAdsCreativeListResponse,
    summary="Get Meta Ads creative metrics",
    description="Retrieve Meta Ads metrics grouped by ad creative. Optionally filter by date range and ad ID."
)
async def get_meta_ads_creatives(
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
    ad_id: Optional[str] = Query(
        default=None,
        description="Filter by specific ad ID",
        example="120237636763120286"
    ),
):
    """
    Get Meta Ads creative metrics including:
    - Ad ID
    - Ad Name
    - Ad Type
    - Spend
    - Impressions
    - Clicks
    - Conversions
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    """
    return meta_ads_creative_service.get_creatives(
        date_from=date_from,
        date_to=date_to,
        ad_id=ad_id
    )
