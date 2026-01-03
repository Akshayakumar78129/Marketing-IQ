"""
Traffic by Source router - API endpoints for traffic source metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import traffic_by_source_service
from .models import TrafficBySourceResponse

router = APIRouter()


@router.get(
    "/traffic-by-source",
    response_model=TrafficBySourceResponse,
    summary="Get traffic by source distribution",
    description="Retrieve session distribution by source/medium. Optionally filter by date range."
)
async def get_traffic_by_source(
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
    Get traffic distribution by source/medium including:
    - Source/Medium combination (e.g., 'google / organic', '(direct) / (none)')
    - Session count per source
    - Total sessions across all sources

    Data is sourced from GA4 analytics.
    """
    return traffic_by_source_service.get_traffic_by_source(
        date_from=date_from,
        date_to=date_to
    )
