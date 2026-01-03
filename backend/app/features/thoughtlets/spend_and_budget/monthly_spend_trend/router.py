"""
Thoughtlets Spend and Budget - Monthly Spend Trend router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import monthly_spend_trend_service
from .models import MonthlySpendTrendResponse

router = APIRouter()


@router.get(
    "/monthly-spend-trend",
    response_model=MonthlySpendTrendResponse,
    summary="Get monthly spend trend data",
    description="Retrieve marketing investment over time aggregated by month. Optionally filter by date range."
)
async def get_monthly_spend_trend(
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
    Get monthly spend trend data including:
    - Month (YYYY-MM format)
    - Total spend for each month

    Data is aggregated from all advertising platforms (Google Ads, Meta Ads, etc.).
    """
    return monthly_spend_trend_service.get_monthly_spend_trend(
        date_from=date_from,
        date_to=date_to
    )
