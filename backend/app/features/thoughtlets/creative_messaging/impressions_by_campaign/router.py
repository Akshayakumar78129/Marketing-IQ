"""
Creative & Messaging - Impressions by Campaign router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import impressions_by_campaign_service
from .models import ImpressionsByCampaignResponse

router = APIRouter()


@router.get(
    "/impressions-by-campaign",
    response_model=ImpressionsByCampaignResponse,
    summary="Get impressions by campaign",
    description="Returns top campaigns by impressions for bar chart visualization."
)
def get_impressions_by_campaign(
    date_from: Optional[date] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date for filtering (YYYY-MM-DD)"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of campaigns to return")
) -> ImpressionsByCampaignResponse:
    """Get top campaigns by impressions for bar chart."""
    return impressions_by_campaign_service.get_impressions_by_campaign(
        date_from=date_from,
        date_to=date_to,
        limit=limit
    )
