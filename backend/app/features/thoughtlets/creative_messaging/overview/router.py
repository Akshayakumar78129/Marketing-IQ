"""
Creative & Messaging - Overview router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import overview_service
from .models import OverviewResponse

router = APIRouter()


@router.get(
    "/overview",
    response_model=OverviewResponse,
    summary="Get Creative & Messaging overview metrics",
    description="Retrieve KPI metrics for creatives including counts, CTR, CPC, CPM, and ROAS."
)
async def get_overview_metrics(
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
    Get Creative & Messaging overview KPI metrics:
    - Total Creatives
    - Image Creatives
    - Video Creatives
    - Average CTR
    - Average CPC
    - CPM
    - Overall ROAS

    Data is aggregated from creatives with performance data in the date range.
    """
    return overview_service.get_overview_metrics(
        date_from=date_from,
        date_to=date_to
    )
