"""
GA4 Analytics Hourly Traffic Pattern router - API endpoints for hourly traffic operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import ga4_hourly_traffic_pattern_service
from .models import HourlyTrafficPatternResponse

router = APIRouter()


@router.get(
    "/hourly-traffic-pattern",
    response_model=HourlyTrafficPatternResponse,
    summary="Get GA4 hourly traffic pattern",
    description="Retrieve hourly impressions and clicks for traffic pattern analysis. Optionally filter by date range."
)
async def get_hourly_traffic_pattern(
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
    Get GA4 Analytics hourly traffic pattern including:
    - Hour (0-23)
    - Hour label (12 AM, 1 PM, etc.)
    - Impressions per hour
    - Clicks per hour

    Results are ordered by hour in ascending order (0-23) for chart rendering.
    """
    return ga4_hourly_traffic_pattern_service.get_hourly_traffic_pattern(
        date_from=date_from,
        date_to=date_to
    )
