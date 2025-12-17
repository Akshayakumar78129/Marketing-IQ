"""
Google Ads Daily Performance Trend router - API endpoints for daily performance operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import daily_performance_trend_service
from .models import DailyPerformanceTrendResponse

router = APIRouter()


@router.get(
    "/daily-performance-trend",
    response_model=DailyPerformanceTrendResponse,
    summary="Get Google Ads daily performance trend",
    description="Retrieve Google Ads performance trend by day of week with optional date range filters."
)
async def get_daily_performance_trend(
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
    Get Google Ads daily performance trend including:
    - Day Name (Monday, Tuesday, etc.)
    - Day Order (for sorting: 1=Monday through 7=Sunday)
    - Total Conversions
    - Total Spend
    """
    return daily_performance_trend_service.get_daily_performance_trend(
        date_from=date_from,
        date_to=date_to
    )
