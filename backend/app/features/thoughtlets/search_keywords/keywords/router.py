"""
Search & Keywords - Keywords Performance router - API endpoints.
"""
from datetime import date
from typing import Optional, Literal
from fastapi import APIRouter, Query

from .service import keywords_service
from .models import KeywordsListResponse

router = APIRouter()


@router.get(
    "/keywords",
    response_model=KeywordsListResponse,
    summary="Get all keywords performance",
    description="Retrieve all keywords with their performance metrics. Used for the All Keywords Performance table."
)
async def get_keywords_performance(
    date_from: Optional[date] = Query(
        default=None,
        description="Start date for metrics (YYYY-MM-DD format)",
        example="2024-01-01"
    ),
    date_to: Optional[date] = Query(
        default=None,
        description="End date for metrics (YYYY-MM-DD format)",
        example="2024-12-31"
    ),
    match_type: Optional[Literal["EXACT", "PHRASE", "BROAD"]] = Query(
        default=None,
        description="Filter by match type"
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=500,
        description="Number of keywords to return (1-500)"
    ),
):
    """
    Get all keywords with performance metrics for the table view:
    - Keyword text
    - Match type
    - Impressions, Clicks, CTR
    - CPC, Spend
    - Conversions, Conversion Rate
    """
    return keywords_service.get_keywords_performance(
        date_from=date_from,
        date_to=date_to,
        match_type=match_type,
        limit=limit
    )
