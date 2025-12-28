"""
GA4 Analytics Landing Pages router - API endpoints for landing page operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import ga4_landing_pages_service
from .models import LandingPagesResponse

router = APIRouter()


@router.get(
    "/landing-pages",
    response_model=LandingPagesResponse,
    summary="Get GA4 landing pages by entrances",
    description="Retrieve landing pages (entry points for user sessions) ranked by entrances. Optionally filter by date range."
)
async def get_landing_pages(
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
    Get GA4 Analytics landing pages including:
    - Page path
    - Entrances (entry points)
    - Bounce rate
    - Sessions

    Results are ordered by entrances in descending order.
    """
    return ga4_landing_pages_service.get_landing_pages(
        date_from=date_from,
        date_to=date_to
    )
