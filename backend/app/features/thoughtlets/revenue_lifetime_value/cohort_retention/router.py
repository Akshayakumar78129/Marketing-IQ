"""
Revenue & Lifetime Value - Cohort Retention router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import cohort_retention_service
from .models import CohortRetentionResponse

router = APIRouter()


@router.get(
    "/cohort-retention",
    response_model=CohortRetentionResponse,
    summary="Get cohort retention table data",
    description="Retrieve cohort retention data with monthly cohorts and retention metrics."
)
async def get_cohort_retention(
    date_from: Optional[date] = Query(
        default=None,
        description="Start date for cohorts (YYYY-MM-DD format). If not provided, no start date filter.",
        example="2024-01-01"
    ),
    date_to: Optional[date] = Query(
        default=None,
        description="End date for cohorts (YYYY-MM-DD format). If not provided, no end date filter.",
        example="2024-12-31"
    ),
    limit: int = Query(
        default=12,
        ge=1,
        le=100,
        description="Number of cohorts to return (default: 12)"
    ),
):
    """
    Get cohort retention data for the table:
    - Cohort month
    - Initial size (new customers)
    - Retained counts at 30, 60, 90 days
    - Retention rates at 30, 60, 90 days

    Returns the most recent cohorts first.
    """
    return cohort_retention_service.get_cohort_retention(
        date_from=date_from,
        date_to=date_to,
        limit=limit
    )
