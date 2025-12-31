"""
Revenue & Lifetime Value - Customer Types router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import customer_types_service
from .models import CustomerTypesResponse

router = APIRouter()


@router.get(
    "/customer-types",
    response_model=CustomerTypesResponse,
    summary="Get customer type distribution",
    description="Retrieve customer counts by type (New, Repeat, One-Time) for pie chart visualization."
)
async def get_customer_types(
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
    Get customer type distribution:
    - New Customers
    - Repeat Customers
    - One-Time Customers

    Returns customer count for each type.
    """
    return customer_types_service.get_customer_types(
        date_from=date_from,
        date_to=date_to
    )
