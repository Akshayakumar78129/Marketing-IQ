"""
Creative & Messaging - CTA Types router - API endpoints.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import cta_types_service
from .models import CTATypesResponse

router = APIRouter()


@router.get(
    "/cta-types",
    response_model=CTATypesResponse,
    summary="Get CTA type distribution",
    description="Returns call-to-action type distribution for bar chart visualization."
)
def get_cta_types(
    date_from: Optional[date] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date for filtering (YYYY-MM-DD)")
) -> CTATypesResponse:
    """Get CTA type distribution for bar chart."""
    return cta_types_service.get_cta_types(
        date_from=date_from,
        date_to=date_to
    )
