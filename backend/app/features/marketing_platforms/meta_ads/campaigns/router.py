"""
Meta Ads Campaigns router - API endpoints for campaign operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import meta_ads_campaigns_service
from .models import MetaAdsCampaignsListResponse

router = APIRouter()


@router.get(
    "/campaigns",
    response_model=MetaAdsCampaignsListResponse,
    summary="Get Meta Ads campaigns",
    description="Retrieve list of Meta Ads campaigns with aggregated metrics. Optionally filter by date range and status."
)
async def get_meta_ads_campaigns(
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
    status: Optional[str] = Query(
        default=None,
        description="Filter by campaign status (e.g., ACTIVE, PAUSED)",
        example="ACTIVE"
    ),
):
    """
    Get Meta Ads campaigns with metrics including:
    - Campaign ID and Name
    - Status
    - Total Spend
    - Impressions
    - Clicks
    - Conversions
    - Revenue
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    - CPM (Cost Per Mille)
    - ROAS (Return on Ad Spend)
    """
    return meta_ads_campaigns_service.get_campaigns(
        date_from=date_from,
        date_to=date_to,
        status=status
    )
