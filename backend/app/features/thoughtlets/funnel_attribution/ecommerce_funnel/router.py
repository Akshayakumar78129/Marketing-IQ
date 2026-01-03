"""
eCommerce Funnel router - API endpoints for eCommerce funnel metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import ecommerce_funnel_service
from .models import EcommerceFunnelResponse

router = APIRouter()


@router.get(
    "/ecommerce-funnel",
    response_model=EcommerceFunnelResponse,
    summary="Get eCommerce funnel metrics",
    description="Retrieve eCommerce funnel metrics showing the View → Cart → Purchase journey. Optionally filter by date range."
)
async def get_ecommerce_funnel(
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
    Get eCommerce funnel metrics including:
    - Views: Total number of product views
    - Add to Cart: Total number of items added to cart
    - Purchase: Total number of items purchased

    This represents the View → Cart → Purchase journey.
    """
    return ecommerce_funnel_service.get_funnel(
        date_from=date_from,
        date_to=date_to
    )
