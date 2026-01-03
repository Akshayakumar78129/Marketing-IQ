"""
Engagement Funnel router - API endpoints for engagement funnel metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import engagement_funnel_service
from .models import EngagementFunnelResponse

router = APIRouter()


@router.get(
    "/engagement-funnel",
    response_model=EngagementFunnelResponse,
    summary="Get engagement funnel metrics",
    description="Retrieve engagement funnel metrics showing user journey from visit to conversion. Optionally filter by date range."
)
async def get_engagement_funnel(
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
    Get engagement funnel metrics including:
    - Total Users: Unique users who visited
    - Sessions: Total number of sessions
    - Engaged: Number of engaged sessions
    - Conversions: Total conversions

    Data is sourced from GA4 analytics.
    """
    return engagement_funnel_service.get_engagement_funnel(
        date_from=date_from,
        date_to=date_to
    )
