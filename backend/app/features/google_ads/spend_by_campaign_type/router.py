"""
Google Ads Spend by Campaign Type router - API endpoints for spend breakdown operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import spend_by_campaign_type_service
from .models import SpendByCampaignTypeResponse

router = APIRouter()


@router.get(
    "/spend-by-campaign-type",
    response_model=SpendByCampaignTypeResponse,
    summary="Get Google Ads spend by campaign type",
    description="Retrieve Google Ads spend breakdown by campaign type with optional date range filters."
)
async def get_spend_by_campaign_type(
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
    Get Google Ads spend breakdown by campaign type including:
    - Campaign Type (Search, Shopping, Performance Max, Video, Demand Gen, Display)
    - Total Spend
    - Spend Percentage (of total Google Ads spend)
    """
    return spend_by_campaign_type_service.get_spend_by_campaign_type(
        date_from=date_from,
        date_to=date_to
    )
