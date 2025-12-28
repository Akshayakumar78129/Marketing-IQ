"""
Meta Ads Demographics Age router - API endpoints for age demographic metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import meta_ads_demographics_age_service
from .models import MetaAdsDemographicsAgeListResponse

router = APIRouter()


@router.get(
    "/demographics/age",
    response_model=MetaAdsDemographicsAgeListResponse,
    summary="Get Meta Ads age demographics",
    description="Retrieve Meta Ads metrics grouped by age bracket. Optionally filter by date range and age bracket."
)
async def get_meta_ads_demographics_age(
    date_from: Optional[date] = Query(
        default=None,
        description="Start date for metrics (YYYY-MM-DD format). If not provided, no start date filter.",
        example="2025-11-15"
    ),
    date_to: Optional[date] = Query(
        default=None,
        description="End date for metrics (YYYY-MM-DD format). If not provided, no end date filter.",
        example="2025-12-15"
    ),
    age_bracket: Optional[str] = Query(
        default=None,
        description="Filter by specific age bracket (18-24, 25-34, 35-44, 45-54, 55-64, 65+)",
        example="25-34"
    ),
):
    """
    Get Meta Ads age demographic metrics including:
    - Age Bracket
    - Impressions
    - Spend
    - Clicks
    - Reach
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    """
    return meta_ads_demographics_age_service.get_demographics_age(
        date_from=date_from,
        date_to=date_to,
        age_bracket=age_bracket
    )
