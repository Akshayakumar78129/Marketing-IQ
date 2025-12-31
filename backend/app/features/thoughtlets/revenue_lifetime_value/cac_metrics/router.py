"""
Revenue & Lifetime Value - CAC Metrics router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import cac_metrics_service
from .models import CACMetricsResponse

router = APIRouter()


@router.get(
    "/cac-metrics",
    response_model=CACMetricsResponse,
    summary="Get Customer Acquisition Cost metrics",
    description="Retrieve CAC metrics by platform (Google Ads, Meta Ads) and total spend."
)
async def get_cac_metrics(
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
    Get Customer Acquisition Cost metrics:
    - Google Ads CAC
    - Meta Ads CAC
    - Blended CAC
    - Platform-specific spend

    Data is aggregated from cohort metrics.
    """
    return cac_metrics_service.get_cac_metrics(
        date_from=date_from,
        date_to=date_to
    )
