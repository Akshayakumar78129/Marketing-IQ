"""
Thoughtlets Spend and Budget - Spend by Campaign router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import spend_by_campaign_service
from .models import SpendByCampaignResponse

router = APIRouter()


@router.get(
    "/spend-by-campaign",
    response_model=SpendByCampaignResponse,
    summary="Get spend by campaign",
    description="Retrieve budget allocation across all campaigns with filters."
)
async def get_spend_by_campaign(
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
    platform: Optional[str] = Query(
        default=None,
        description="Filter by platform (e.g., 'Google Ads', 'Meta Ads')",
        example="Google Ads"
    ),
    status: Optional[str] = Query(
        default=None,
        description="Filter by campaign status (e.g., 'ENABLED', 'ACTIVE')",
        example="ENABLED"
    ),
):
    """
    Get spend by campaign including:
    - Campaign name
    - Platform
    - Status
    - Spend
    - Revenue
    - ROAS (Return on Ad Spend)
    - Conversions
    - CPC (Cost per Click)

    Supports filtering by platform and status.
    """
    return spend_by_campaign_service.get_spend_by_campaign(
        date_from=date_from,
        date_to=date_to,
        platform=platform,
        campaign_status=status
    )
