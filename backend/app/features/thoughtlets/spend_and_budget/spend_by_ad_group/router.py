"""
Thoughtlets Spend and Budget - Spend by Ad Group router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import spend_by_ad_group_service
from .models import SpendByAdGroupResponse

router = APIRouter()


@router.get(
    "/spend-by-ad-group",
    response_model=SpendByAdGroupResponse,
    summary="Get spend by ad group",
    description="Retrieve budget utilization at ad group level."
)
async def get_spend_by_ad_group(
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
    Get spend by ad group including:
    - Ad group name (Campaign)
    - Impressions
    - Clicks
    - Spend
    - Conversions
    - ROAS (Return on Ad Spend)
    """
    return spend_by_ad_group_service.get_spend_by_ad_group(
        date_from=date_from,
        date_to=date_to
    )
