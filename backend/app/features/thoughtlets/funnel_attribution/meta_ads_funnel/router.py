"""
Meta Ads Funnel router - API endpoints for Meta pixel conversion events.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import meta_ads_funnel_service
from .models import MetaAdsFunnelResponse

router = APIRouter()


@router.get(
    "/meta-ads-funnel",
    response_model=MetaAdsFunnelResponse,
    summary="Get Meta Ads funnel metrics",
    description="Retrieve Meta Ads funnel metrics showing pixel conversion events. Optionally filter by date range."
)
async def get_meta_ads_funnel(
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
    Get Meta Ads funnel metrics including:
    - View Content: Total View Content pixel events
    - Add to Cart: Total Add to Cart pixel events
    - Initiate Checkout: Total Initiate Checkout pixel events
    - Purchase: Total Purchase pixel events

    This represents the Meta pixel conversion events funnel.
    """
    return meta_ads_funnel_service.get_funnel(
        date_from=date_from,
        date_to=date_to
    )
