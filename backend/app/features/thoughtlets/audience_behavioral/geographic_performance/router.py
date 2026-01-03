"""
Geographic Performance router - API endpoints for geo performance metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import geographic_performance_service
from .models import GeographicPerformanceResponse

router = APIRouter()


@router.get(
    "/geographic-performance",
    response_model=GeographicPerformanceResponse,
    summary="Get geographic performance metrics",
    description="Retrieve user metrics by country/region. Optionally filter by date range."
)
async def get_geographic_performance(
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
    Get geographic performance metrics by country including:
    - Users
    - New Users
    - New User %
    - Engaged (sessions)
    - Eng. Rate %

    Data is sourced from GA4 analytics.
    """
    return geographic_performance_service.get_geographic_performance(
        date_from=date_from,
        date_to=date_to
    )
