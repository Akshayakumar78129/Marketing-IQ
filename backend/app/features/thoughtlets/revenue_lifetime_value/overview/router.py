"""
Revenue & Lifetime Value Overview router - API endpoints for CLV metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import revenue_overview_service
from .models import RevenueOverviewResponse

router = APIRouter()


@router.get(
    "/overview",
    response_model=RevenueOverviewResponse,
    summary="Get revenue and lifetime value overview metrics",
    description="Retrieve aggregated CLV metrics including total revenue, average CLV, repeat purchase rate, and churn risk."
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
    Get aggregated revenue and lifetime value overview metrics including:
    - Total Revenue
    - Average CLV (Customer Lifetime Value)
    - Historic CLV
    - Predicted CLV
    - Repeat Purchase Rate
    - CLV:CAC Ratio
    - Average AOV (Average Order Value)
    - Churn Risk percentage
    """
    return revenue_overview_service.get_overview(
        date_from=date_from,
        date_to=date_to
    )
