"""
Google Ads Campaign Performance router - API endpoints for campaign performance operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import campaign_performance_service
from .models import CampaignPerformanceListResponse

router = APIRouter()


@router.get(
    "/campaign-performance",
    response_model=CampaignPerformanceListResponse,
    summary="Get Google Ads campaign performance",
    description="Retrieve Google Ads campaign performance metrics with optional filters for date range and status."
)
async def get_campaign_performance(
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
    status: Optional[str] = Query(
        default=None,
        description="Filter by campaign status (e.g., 'Active', 'Paused'). If not provided, returns all statuses.",
        example="Active"
    ),
):
    """
    Get Google Ads campaign performance metrics including:
    - Campaign Name
    - Status
    - Spend
    - Revenue
    - ROAS (Return on Ad Spend)
    - Conversions
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    """
    return campaign_performance_service.get_campaign_performance(
        date_from=date_from,
        date_to=date_to,
        campaign_status=status
    )
