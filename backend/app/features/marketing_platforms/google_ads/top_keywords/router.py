"""
Google Ads Top Keywords router - API endpoints for top keywords operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import top_keywords_service
from .models import TopKeywordsResponse

router = APIRouter()


@router.get(
    "/top-keywords",
    response_model=TopKeywordsResponse,
    summary="Get Google Ads top keywords",
    description="Retrieve Google Ads top keywords by impressions with optional date range filters."
)
async def get_top_keywords(
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
    Get Google Ads top keywords metrics including:
    - Keyword Text
    - Match Type (EXACT, PHRASE, BROAD)
    - Impressions
    - Clicks
    - CTR (Click-Through Rate)
    - Conversions
    - Cost (Total Spend)
    """
    return top_keywords_service.get_top_keywords(
        date_from=date_from,
        date_to=date_to
    )
