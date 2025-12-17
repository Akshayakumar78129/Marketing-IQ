"""
Google Ads Keyword Performance router - API endpoints for keyword performance operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import keyword_performance_service
from .models import KeywordPerformanceResponse

router = APIRouter()


@router.get(
    "/keyword-performance",
    response_model=KeywordPerformanceResponse,
    summary="Get Google Ads keyword performance",
    description="Retrieve Google Ads keyword performance metrics with optional date range filters."
)
async def get_keyword_performance(
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
    Get Google Ads keyword performance metrics including:
    - Keyword Text
    - Match Type (EXACT, PHRASE, BROAD)
    - Impressions
    - Clicks
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    - Conversions
    - Cost (Total Spend)
    """
    return keyword_performance_service.get_keyword_performance(
        date_from=date_from,
        date_to=date_to
    )
