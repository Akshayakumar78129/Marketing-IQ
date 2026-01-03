"""
Users by Country router - API endpoints for country metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import users_by_country_service
from .models import UsersByCountryResponse

router = APIRouter()


@router.get(
    "/users-by-country",
    response_model=UsersByCountryResponse,
    summary="Get users by country",
    description="Retrieve user counts by country (geographic distribution). Optionally filter by date range."
)
async def get_users_by_country(
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
    Get user geographic distribution by country including:
    - Country name
    - User count per country
    - Total users across all countries

    Data is sourced from GA4 analytics.
    """
    return users_by_country_service.get_users_by_country(
        date_from=date_from,
        date_to=date_to
    )
