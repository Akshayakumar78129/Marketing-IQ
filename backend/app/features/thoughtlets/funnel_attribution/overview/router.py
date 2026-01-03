"""
Funnel & Attribution Overview router - API endpoints for funnel/attribution metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import funnel_attribution_overview_service
from .models import FunnelAttributionOverviewResponse

router = APIRouter()


@router.get(
    "/overview",
    response_model=FunnelAttributionOverviewResponse,
    summary="Get funnel and attribution overview metrics",
    description="Retrieve aggregated funnel and attribution metrics. Optionally filter by date range."
)
async def get_overview(
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
    Get aggregated funnel and attribution metrics including:
    - Total Sessions
    - Engagement Rate
    - View-to-Cart %
    - Cart-to-Purchase %
    - Cart Abandon Rate
    - Total Conversions
    - UTM Coverage %
    - Average Order Value

    Data is aggregated from GA4 sessions, ecommerce, and order data.
    """
    return funnel_attribution_overview_service.get_overview(
        date_from=date_from,
        date_to=date_to
    )
