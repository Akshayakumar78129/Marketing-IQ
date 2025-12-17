"""
Meta Ads Device router - API endpoints for device metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import meta_ads_device_service
from .models import MetaAdsDeviceListResponse

router = APIRouter()


@router.get(
    "/device",
    response_model=MetaAdsDeviceListResponse,
    summary="Get Meta Ads device metrics",
    description="Retrieve Meta Ads metrics grouped by device type. Optionally filter by date range and device."
)
async def get_meta_ads_device(
    date_from: Optional[date] = Query(
        default=None,
        description="Start date for metrics (YYYY-MM-DD format). If not provided, no start date filter.",
        example="2025-11-15"
    ),
    date_to: Optional[date] = Query(
        default=None,
        description="End date for metrics (YYYY-MM-DD format). If not provided, no end date filter.",
        example="2025-12-15"
    ),
    device: Optional[str] = Query(
        default=None,
        description="Filter by specific device (mobile_app, desktop, mobile_web)",
        example="mobile_app"
    ),
):
    """
    Get Meta Ads device metrics including:
    - Device type
    - Impressions
    - Reach
    - Spend
    - Clicks
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    """
    return meta_ads_device_service.get_devices(
        date_from=date_from,
        date_to=date_to,
        device=device
    )
