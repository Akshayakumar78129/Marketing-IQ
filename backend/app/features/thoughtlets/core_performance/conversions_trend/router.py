"""
Thoughtlets Core Performance Conversions Trend router - API endpoints for monthly conversions.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import conversions_trend_service
from .models import ConversionsTrendResponse

router = APIRouter()


@router.get(
    "/conversions-trend",
    response_model=ConversionsTrendResponse,
    summary="Get monthly conversions trend across all platforms",
    description="Retrieve monthly conversion volume data for charting. Optionally filter by date range."
)
async def get_conversions_trend(
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
    Get monthly conversions trend including:
    - Month (formatted as 'Jan 2025', 'Feb 2025', etc.)
    - Conversions count for each month

    Data is aggregated from all advertising platforms (Google Ads, Meta, etc.).
    Results are ordered chronologically.
    """
    return conversions_trend_service.get_conversions_trend(
        date_from=date_from,
        date_to=date_to
    )
