"""
GA4 Analytics Geographic Performance router - API endpoints for geographic operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import ga4_geographic_performance_service
from .models import GeographicPerformanceResponse

router = APIRouter()


@router.get(
    "/geographic-performance",
    response_model=GeographicPerformanceResponse,
    summary="Get GA4 geographic performance by country",
    description="Retrieve traffic and conversions by country. Optionally filter by date range."
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
    Get GA4 Analytics geographic performance including:
    - Country name
    - Sessions
    - Conversion rate
    - Revenue

    Results are ordered by sessions in descending order.
    """
    return ga4_geographic_performance_service.get_geographic_performance(
        date_from=date_from,
        date_to=date_to
    )
