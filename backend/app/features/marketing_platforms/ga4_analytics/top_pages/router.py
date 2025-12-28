"""
GA4 Analytics Top Pages router - API endpoints for page operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import ga4_top_pages_service
from .models import TopPagesResponse

router = APIRouter()


@router.get(
    "/top-pages",
    response_model=TopPagesResponse,
    summary="Get GA4 top pages by page views",
    description="Retrieve top pages ranked by page views. Optionally filter by date range."
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
    Get GA4 Analytics top pages including:
    - Page path
    - Page views count
    - Unique views (users)
    - Average time on page (seconds)

    Results are ordered by page views in descending order.
    """
    return ga4_top_pages_service.get_top_pages(
        date_from=date_from,
        date_to=date_to
    )
