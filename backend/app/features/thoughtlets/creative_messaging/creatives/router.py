"""
Creative & Messaging - Creatives router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import creatives_service
from .models import CreativesResponse

router = APIRouter()


@router.get(
    "/creatives",
    response_model=CreativesResponse,
    summary="Get all creatives (paginated)",
    description="Returns paginated list of creatives with performance metrics."
)
def get_creatives(
    date_from: Optional[date] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date for filtering (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page")
) -> CreativesResponse:
    """Get paginated creatives with performance data."""
    return creatives_service.get_creatives(
        date_from=date_from,
        date_to=date_to,
        page=page,
        page_size=page_size
    )
