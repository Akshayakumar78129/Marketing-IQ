"""
Revenue & Lifetime Value - Churn Distribution router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import churn_distribution_service
from .models import ChurnDistributionResponse

router = APIRouter()


@router.get(
    "/churn-distribution",
    response_model=ChurnDistributionResponse,
    summary="Get churn risk distribution",
    description="Retrieve customer distribution by churn risk level for bar chart visualization."
)
async def get_churn_distribution(
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
    Get churn risk distribution:
    - Low Risk
    - Healthy
    - Medium Risk
    - High Risk

    Returns customer count for each risk level.
    """
    return churn_distribution_service.get_churn_distribution(
        date_from=date_from,
        date_to=date_to
    )
