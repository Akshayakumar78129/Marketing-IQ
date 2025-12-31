"""
Search & Keywords Top Keywords router - API endpoints for top keywords.
"""
from datetime import date
from typing import Optional, Literal
from fastapi import APIRouter, Query

from .service import top_keywords_service
from .models import TopKeywordsResponse

router = APIRouter()


@router.get(
    "/top-keywords",
    response_model=TopKeywordsResponse,
    summary="Get top keywords by conversions or clicks",
    description="Retrieve top performing keywords sorted by conversions or clicks. Used for bar chart visualizations."
)
async def get_top_keywords(
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
    sort_by: Literal["conversions", "clicks"] = Query(
        default="conversions",
        description="Sort keywords by 'conversions' or 'clicks'"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of top keywords to return (1-100)"
    ),
):
    """
    Get top keywords for bar chart visualizations:
    - Top Keywords by Conversions
    - Top Keywords by Clicks

    Use the `sort_by` parameter to switch between the two views.
    """
    return top_keywords_service.get_top_keywords(
        date_from=date_from,
        date_to=date_to,
        sort_by=sort_by,
        limit=limit
    )
