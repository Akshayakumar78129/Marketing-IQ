"""
Thoughtlets Core Performance ROAS by Platform router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import roas_by_platform_service
from .models import RoasByPlatformResponse

router = APIRouter()


@router.get(
    "/roas-by-platform",
    response_model=RoasByPlatformResponse,
    summary="Get ROAS by platform",
    description="Retrieve return on ad spend grouped by advertising platform. Optionally filter by date range."
)
async def get_roas_by_platform(
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
    Get ROAS (Return on Ad Spend) by platform including:
    - Platform name (Google Ads, Meta Ads, etc.)
    - ROAS value (revenue / spend)

    Results are ordered by ROAS in descending order.
    """
    return roas_by_platform_service.get_roas_by_platform(
        date_from=date_from,
        date_to=date_to
    )
