"""
Top Pages router - API endpoints for page metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import top_pages_service
from .models import TopPagesResponse

router = APIRouter()


@router.get(
    "/top-pages",
    response_model=TopPagesResponse,
    summary="Get top pages with engagement metrics",
    description="Retrieve most viewed pages with engagement metrics. Optionally filter by date range."
)
async def get_top_pages(
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
    Get top pages with engagement metrics including:
    - Page path
    - Page type (Homepage, Product Page, Collection Page, Checkout, Other)
    - Views (total page views)
    - Users (unique users)
    - Average time on page (seconds)
    - Views per user

    Data is sourced from GA4 analytics.
    """
    return top_pages_service.get_top_pages(
        date_from=date_from,
        date_to=date_to
    )
