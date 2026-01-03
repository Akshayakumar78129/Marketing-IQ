"""
Thoughtlets Spend and Budget - ROAS by Platform router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import roas_by_platform_service
from .models import ROASByPlatformResponse

router = APIRouter()


@router.get(
    "/roas-by-platform",
    response_model=ROASByPlatformResponse,
    summary="Get ROAS breakdown by platform",
    description="Retrieve return on ad spend comparison across different advertising platforms. Optionally filter by date range."
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
    Get ROAS breakdown by platform including:
    - Platform name
    - ROAS (Return on Ad Spend) per platform

    Data is aggregated from all advertising platforms (Google Ads, Meta Ads, etc.).
    """
    return roas_by_platform_service.get_roas_by_platform(
        date_from=date_from,
        date_to=date_to
    )
