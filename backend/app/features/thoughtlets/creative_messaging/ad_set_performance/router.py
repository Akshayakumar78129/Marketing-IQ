"""
Creative & Messaging - Ad Set Performance router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import ad_set_performance_service
from .models import AdSetPerformanceResponse

router = APIRouter()


@router.get(
    "/ad-set-performance",
    response_model=AdSetPerformanceResponse,
    summary="Get ad set performance",
    description="Returns ad set performance metrics for table visualization."
)
def get_ad_set_performance(
    date_from: Optional[date] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date for filtering (YYYY-MM-DD)")
) -> AdSetPerformanceResponse:
    """Get ad set performance data for table."""
    return ad_set_performance_service.get_ad_set_performance(
        date_from=date_from,
        date_to=date_to
    )
