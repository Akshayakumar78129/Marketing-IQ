"""
Search & Keywords Match Type router - API endpoints for match type distribution.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import match_type_service
from .models import MatchTypeResponse

router = APIRouter()


@router.get(
    "/match-type",
    response_model=MatchTypeResponse,
    summary="Get keyword distribution by match type",
    description="Retrieve keyword count and spend distribution across match types (EXACT, PHRASE, BROAD). Used for pie chart and bar chart visualizations."
)
async def get_match_type_distribution(
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
    Get keyword distribution by match type for visualizations:
    - Keywords by Match Type (pie chart - count distribution)
    - Spend by Match Type (bar chart - spend distribution)

    Returns data for EXACT, PHRASE, and BROAD match types.
    """
    return match_type_service.get_match_type_distribution(
        date_from=date_from,
        date_to=date_to
    )
