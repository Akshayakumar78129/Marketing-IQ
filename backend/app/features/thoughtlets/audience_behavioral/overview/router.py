"""
Audience & Behavioral Overview router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import audience_behavioral_overview_service
from .models import AudienceBehavioralOverviewResponse

router = APIRouter()


@router.get(
    "/overview",
    response_model=AudienceBehavioralOverviewResponse,
    summary="Get audience and behavioral overview metrics",
    description="Retrieve aggregated audience and behavioral metrics from GA4 data."
)
async def get_audience_behavioral_overview(
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
    Get audience and behavioral overview metrics including:
    - Total Users
    - Total Sessions
    - New Users
    - Returning Users
    - Engagement Rate
    - Bounce Rate
    - Sessions per User
    - Conversion Rate
    """
    return audience_behavioral_overview_service.get_overview(
        date_from=date_from,
        date_to=date_to
    )
