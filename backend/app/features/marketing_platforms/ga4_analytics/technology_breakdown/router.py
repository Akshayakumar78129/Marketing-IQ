"""
GA4 Analytics Technology Breakdown router - API endpoints for technology breakdown operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import ga4_technology_breakdown_service
from .models import TechnologyBreakdownResponse

router = APIRouter()


@router.get(
    "/technology-breakdown",
    response_model=TechnologyBreakdownResponse,
    summary="Get GA4 technology breakdown metrics",
    description="Retrieve technology breakdown showing traffic sources, devices, and browsers distribution. Optionally filter by date range."
)
async def get_technology_breakdown(
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
    Get GA4 Analytics technology breakdown including:
    - Traffic Sources (sessions by source)
    - Devices (users by device category)
    - Browsers (users by browser)

    Results are ordered by count in descending order for each category.
    """
    return ga4_technology_breakdown_service.get_technology_breakdown(
        date_from=date_from,
        date_to=date_to
    )
