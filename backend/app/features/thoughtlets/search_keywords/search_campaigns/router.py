"""
Search & Keywords - Search Campaigns Performance router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import search_campaigns_service
from .models import SearchCampaignsResponse

router = APIRouter()


@router.get(
    "/search-campaigns",
    response_model=SearchCampaignsResponse,
    summary="Get search campaign performance",
    description="Retrieve search campaign performance metrics for SEARCH and PERFORMANCE_MAX campaign types."
)
async def get_search_campaigns(
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
):
    """
    Get search campaign performance for the table view:
    - Campaign name
    - Type (SEARCH, PERFORMANCE_MAX)
    - Status
    - Impressions, Clicks, CTR
    - Spend, Conversions, ROAS
    """
    return search_campaigns_service.get_search_campaigns(
        date_from=date_from,
        date_to=date_to
    )
