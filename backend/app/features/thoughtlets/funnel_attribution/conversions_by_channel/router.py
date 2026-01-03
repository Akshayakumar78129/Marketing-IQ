"""
Conversions by Channel router - API endpoints for channel conversion metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import conversions_by_channel_service
from .models import ConversionsByChannelResponse

router = APIRouter()


@router.get(
    "/conversions-by-channel",
    response_model=ConversionsByChannelResponse,
    summary="Get conversions by marketing channel",
    description="Retrieve conversion metrics grouped by marketing channel. Optionally filter by date range."
)
async def get_conversions_by_channel(
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
    Get conversions grouped by marketing channel including:
    - Direct
    - Organic Search
    - Paid Search
    - Email
    - Referral
    - Paid Social
    - Display
    - Other

    Each channel includes total conversions and revenue.
    """
    return conversions_by_channel_service.get_conversions_by_channel(
        date_from=date_from,
        date_to=date_to
    )
