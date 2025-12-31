"""
Revenue & Lifetime Value - Customer Segments router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import customer_segments_service
from .models import CustomerSegmentsResponse

router = APIRouter()


@router.get(
    "/customer-segments",
    response_model=CustomerSegmentsResponse,
    summary="Get customers by CLV segment",
    description="Retrieve customer distribution by CLV segment for pie chart visualization."
)
async def get_customer_segments(
    date_from: Optional[date] = Query(
        default=None,
        description="Start date for filtering customers by first order date (YYYY-MM-DD format).",
        example="2024-01-01"
    ),
    date_to: Optional[date] = Query(
        default=None,
        description="End date for filtering customers by first order date (YYYY-MM-DD format).",
        example="2024-12-31"
    ),
):
    """
    Get customer distribution by CLV segment:
    - New/Minimal
    - Low Value
    - Medium Value
    - High Value

    Returns customer count for each segment.
    """
    return customer_segments_service.get_customer_segments(
        date_from=date_from,
        date_to=date_to
    )
