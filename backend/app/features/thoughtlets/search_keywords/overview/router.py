"""
Search & Keywords Overview router - API endpoints for keyword metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import search_keywords_overview_service
from .models import SearchKeywordsOverviewResponse

router = APIRouter()


@router.get(
    "/overview",
    response_model=SearchKeywordsOverviewResponse,
    summary="Get search keywords overview metrics",
    description="Retrieve aggregated keyword performance metrics including match type distribution, CTR, CPC, conversions and spend."
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
    Get aggregated search keywords overview metrics including:
    - Total Keywords count
    - Match type distribution (Exact, Phrase, Broad)
    - Average CTR (Click-Through Rate)
    - Average CPC (Cost per Click)
    - Total Conversions
    - Total Spend

    Data is from Google Ads keyword performance.
    """
    return search_keywords_overview_service.get_overview(
        date_from=date_from,
        date_to=date_to
    )
