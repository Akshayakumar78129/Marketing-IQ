"""
Revenue & Lifetime Value - CLV Breakdown router - API endpoints.
"""
from fastapi import APIRouter

from .service import clv_breakdown_service
from .models import CLVBreakdownResponse

router = APIRouter()


@router.get(
    "/clv-breakdown",
    response_model=CLVBreakdownResponse,
    summary="Get CLV breakdown",
    description="Retrieve overall CLV averages (historic, predicted, total) across all customers."
)
async def get_clv_breakdown():
    """
    Get overall CLV breakdown:
    - Historic CLV (average)
    - Predicted CLV (average)
    - Total CLV (average)

    Note: CLV values are customer-level metrics and are not filtered by date.
    """
    return clv_breakdown_service.get_clv_breakdown()
