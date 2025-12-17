"""
Meta Ads Engagement router - API endpoints for engagement operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import meta_ads_engagement_service
from .models import MetaAdsEngagementResponse

router = APIRouter()


@router.get(
    "/engagement",
    response_model=MetaAdsEngagementResponse,
    summary="Get Meta Ads engagement metrics",
    description="Retrieve aggregated Meta Ads engagement metrics. Optionally filter by date range."
)
async def get_meta_ads_engagement(
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
    Get Meta Ads engagement metrics including:
    - Link Clicks
    - Post Engagements
    - Page Engagements
    - Post Reactions
    - View Content
    - Add to Cart
    - Initiate Checkout
    - Purchases
    - Total Actions
    - View to Cart Rate
    - Cart to Checkout Rate
    - Checkout to Purchase Rate
    """
    return meta_ads_engagement_service.get_engagement(
        date_from=date_from,
        date_to=date_to
    )
