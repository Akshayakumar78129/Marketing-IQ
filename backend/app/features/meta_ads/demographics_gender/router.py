"""
Meta Ads Demographics Gender router - API endpoints for gender demographic metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import meta_ads_demographics_gender_service
from .models import MetaAdsDemographicsGenderListResponse

router = APIRouter()


@router.get(
    "/demographics/gender",
    response_model=MetaAdsDemographicsGenderListResponse,
    summary="Get Meta Ads gender demographics",
    description="Retrieve Meta Ads metrics grouped by gender. Optionally filter by date range and gender."
)
async def get_meta_ads_demographics_gender(
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
    gender: Optional[str] = Query(
        default=None,
        description="Filter by specific gender (male, female, unknown)",
        example="female"
    ),
):
    """
    Get Meta Ads gender demographic metrics including:
    - Gender
    - Impressions
    - Spend
    - Clicks
    - Reach
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    """
    return meta_ads_demographics_gender_service.get_demographics_gender(
        date_from=date_from,
        date_to=date_to,
        gender=gender
    )
