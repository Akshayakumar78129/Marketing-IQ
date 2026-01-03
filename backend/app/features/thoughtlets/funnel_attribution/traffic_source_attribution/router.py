"""
Traffic Source Attribution router - API endpoints for traffic source attribution metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import traffic_source_attribution_service
from .models import TrafficSourceAttributionResponse

router = APIRouter()


@router.get(
    "/traffic-source-attribution",
    response_model=TrafficSourceAttributionResponse,
    summary="Get traffic source attribution data",
    description="Retrieve session and engagement attribution data grouped by source/medium. Optionally filter by date range."
)
async def get_traffic_source_attribution(
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
    Get traffic source attribution data including:
    - Source/Medium combination
    - Sessions from each source
    - Engaged sessions
    - Unique users
    - Engagement rate percentage
    - Sessions per user

    Data is aggregated from GA4 traffic metrics.
    """
    return traffic_source_attribution_service.get_traffic_source_attribution(
        date_from=date_from,
        date_to=date_to
    )
