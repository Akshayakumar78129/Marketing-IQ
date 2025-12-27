"""
GA4 Analytics Traffic Sources router - API endpoints for traffic sources operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import ga4_traffic_sources_service
from .models import TrafficSourcesListResponse

router = APIRouter()


@router.get(
    "/traffic-sources",
    response_model=TrafficSourcesListResponse,
    summary="Get GA4 traffic sources",
    description="Retrieve traffic sources with sessions, users, and revenue metrics. Optionally filter by date range."
)
async def get_traffic_sources(
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
    Get GA4 Analytics traffic sources including:
    - Source name
    - Sessions
    - Users
    - Revenue

    Results are ordered by sessions in descending order.
    """
    return ga4_traffic_sources_service.get_traffic_sources(
        date_from=date_from,
        date_to=date_to
    )
