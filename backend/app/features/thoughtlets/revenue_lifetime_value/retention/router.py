"""
Revenue & Lifetime Value - Retention router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import retention_service
from .models import RetentionResponse

router = APIRouter()


@router.get(
    "/retention",
    response_model=RetentionResponse,
    summary="Get retention metrics by period",
    description="Retrieve retention rates and counts for 30, 60, and 90 day periods."
)
async def get_retention(
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
    Get retention metrics by period:
    - 30-day retention rate and count
    - 60-day retention rate and count
    - 90-day retention rate and count

    Data is aggregated from cohort metrics.
    """
    return retention_service.get_retention(
        date_from=date_from,
        date_to=date_to
    )
