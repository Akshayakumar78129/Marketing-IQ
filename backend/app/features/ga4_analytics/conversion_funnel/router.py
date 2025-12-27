"""
GA4 Analytics Conversion Funnel router - API endpoints for conversion funnel operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import ga4_conversion_funnel_service
from .models import ConversionFunnelResponse

router = APIRouter()


@router.get(
    "/conversion-funnel",
    response_model=ConversionFunnelResponse,
    summary="Get GA4 conversion funnel metrics",
    description="Retrieve conversion funnel metrics showing user journey from session to purchase. Optionally filter by date range."
)
async def get_conversion_funnel(
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
    Get GA4 Analytics conversion funnel metrics including:
    - Sessions (session_start events)
    - Product Views (view_item events)
    - Add to Cart (add_to_cart events)
    - Purchases (purchase events)

    These metrics represent the user journey from session to purchase.
    """
    return ga4_conversion_funnel_service.get_conversion_funnel(
        date_from=date_from,
        date_to=date_to
    )
