"""
Users by Device Type router - API endpoints for device type metrics.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import users_by_device_service
from .models import UsersByDeviceResponse

router = APIRouter()


@router.get(
    "/users-by-device",
    response_model=UsersByDeviceResponse,
    summary="Get users by device type",
    description="Retrieve user counts by device category (desktop, mobile, tablet, etc.). Optionally filter by date range."
)
async def get_users_by_device(
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
    Get user breakdown by device type including:
    - Device category (desktop, mobile, tablet, Unknown)
    - User count per device type
    - Total users across all device types

    Data is sourced from GA4 analytics.
    """
    return users_by_device_service.get_users_by_device(
        date_from=date_from,
        date_to=date_to
    )
