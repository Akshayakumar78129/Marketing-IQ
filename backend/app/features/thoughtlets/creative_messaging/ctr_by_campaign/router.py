"""
Creative & Messaging - CTR by Campaign router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import ctr_by_campaign_service
from .models import CTRByCampaignResponse

router = APIRouter()


@router.get(
    "/ctr-by-campaign",
    response_model=CTRByCampaignResponse,
    summary="Get CTR by campaign",
    description="Returns top campaigns by Click-Through Rate for bar chart visualization."
)
def get_ctr_by_campaign(
    date_from: Optional[date] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date for filtering (YYYY-MM-DD)"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of campaigns to return")
) -> CTRByCampaignResponse:
    """Get top campaigns by CTR for bar chart."""
    return ctr_by_campaign_service.get_ctr_by_campaign(
        date_from=date_from,
        date_to=date_to,
        limit=limit
    )
