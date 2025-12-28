"""
Meta Ads Placements router - API endpoints for placement metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import meta_ads_placements_service
from .models import MetaAdsPlacementsListResponse

router = APIRouter()


@router.get(
    "/placements",
    response_model=MetaAdsPlacementsListResponse,
    summary="Get Meta Ads placements",
    description="Retrieve Meta Ads placement metrics (facebook, instagram, etc.). Optionally filter by date range and placement."
)
async def get_meta_ads_placements(
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
    placement: Optional[str] = Query(
        default=None,
        description="Filter by specific placement (facebook, instagram, audience_network, threads, messenger)",
        example="facebook"
    ),
):
    """
    Get Meta Ads placement metrics including:
    - Placement name
    - Impressions
    - Reach
    - Spend
    - Clicks
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    """
    return meta_ads_placements_service.get_placements(
        date_from=date_from,
        date_to=date_to,
        placement=placement
    )
