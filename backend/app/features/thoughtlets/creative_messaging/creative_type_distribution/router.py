"""
Creative & Messaging - Creative Type Distribution router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import creative_type_distribution_service
from .models import CreativeTypeDistributionResponse

router = APIRouter()


@router.get(
    "/creative-type-distribution",
    response_model=CreativeTypeDistributionResponse,
    summary="Get creative type distribution",
    description="Returns creative type distribution (image vs video) for pie chart visualization."
)
def get_creative_type_distribution(
    date_from: Optional[date] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date for filtering (YYYY-MM-DD)")
) -> CreativeTypeDistributionResponse:
    """Get creative type distribution for pie chart."""
    return creative_type_distribution_service.get_creative_type_distribution(
        date_from=date_from,
        date_to=date_to
    )
