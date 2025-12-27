"""
GA4 Analytics Daily Traffic Trend router - API endpoints for daily traffic operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import ga4_daily_traffic_trend_service
from .models import DailyTrafficTrendResponse

router = APIRouter()


@router.get(
    "/daily-traffic-trend",
    response_model=DailyTrafficTrendResponse,
    summary="Get GA4 daily traffic trend",
    description="Retrieve daily sessions and users over time for trend charts. Optionally filter by date range."
)
async def get_daily_traffic_trend(
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
    Get GA4 Analytics daily traffic trend including:
    - Date
    - Sessions per day
    - Users per day

    Results are ordered by date in ascending order (oldest first) for chart rendering.
    """
    return ga4_daily_traffic_trend_service.get_daily_traffic_trend(
        date_from=date_from,
        date_to=date_to
    )
