"""
Thoughtlets Core Performance Revenue vs Spend router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import revenue_vs_spend_service
from .models import RevenueVsSpendResponse

router = APIRouter()


@router.get(
    "/revenue-vs-spend",
    response_model=RevenueVsSpendResponse,
    summary="Get revenue vs spend comparison by month",
    description="Retrieve monthly revenue and spend data for charting. Optionally filter by date range."
)
async def get_revenue_vs_spend(
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
    Get monthly revenue vs spend comparison including:
    - Month (formatted as 'Jan 2025', 'Feb 2025', etc.)
    - Revenue (conversion value)
    - Spend (ad spend)

    Data is aggregated from all advertising platforms.
    Results are ordered chronologically.
    """
    return revenue_vs_spend_service.get_revenue_vs_spend(
        date_from=date_from,
        date_to=date_to
    )
