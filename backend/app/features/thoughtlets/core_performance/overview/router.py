"""
Thoughtlets Core Performance Overview router - API endpoints for aggregated metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import core_performance_overview_service
from .models import CorePerformanceOverviewResponse

router = APIRouter()


@router.get(
    "/overview",
    response_model=CorePerformanceOverviewResponse,
    summary="Get core performance overview metrics across all platforms",
    description="Retrieve aggregated performance metrics from all advertising platforms. Optionally filter by date range."
)
async def get_overview(
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
    Get aggregated core performance metrics including:
    - Conversions
    - Conversion Rate
    - Cost per Conversion
    - Revenue
    - ROAS (Return on Ad Spend)
    - CTR (Click-Through Rate)
    - CPC (Cost per Click)
    - Impressions

    Data is aggregated from all advertising platforms (Google Ads, Meta, etc.).
    """
    return core_performance_overview_service.get_overview(
        date_from=date_from,
        date_to=date_to
    )
