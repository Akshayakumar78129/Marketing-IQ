"""
Thoughtlets Spend and Budget Overview router - API endpoints for spend/budget metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import spend_and_budget_overview_service
from .models import SpendAndBudgetOverviewResponse

router = APIRouter()


@router.get(
    "/overview",
    response_model=SpendAndBudgetOverviewResponse,
    summary="Get spend and budget overview metrics across all platforms",
    description="Retrieve aggregated spend and budget metrics from all advertising platforms. Optionally filter by date range."
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
    Get aggregated spend and budget metrics including:
    - Total Spend
    - Total Revenue
    - Overall ROAS (Return on Ad Spend)
    - Cost per Conversion
    - Average CPC (Cost per Click)
    - Average Daily Spend
    - Total Impressions
    - Conversions

    Data is aggregated from all advertising platforms (Google Ads, Meta, etc.).
    """
    return spend_and_budget_overview_service.get_overview(
        date_from=date_from,
        date_to=date_to
    )
