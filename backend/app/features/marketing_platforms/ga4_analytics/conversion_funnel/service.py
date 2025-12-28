"""
GA4 Analytics Conversion Funnel service - Business logic layer for conversion funnel operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import ga4_conversion_funnel_repository
from .models import ConversionFunnelResponse


class GA4ConversionFunnelService:
    """Service class for GA4 Analytics conversion funnel business logic."""

    def __init__(self, repository=ga4_conversion_funnel_repository):
        self.repository = repository

    def get_conversion_funnel(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> ConversionFunnelResponse:
        """
        Get conversion funnel metrics, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            ConversionFunnelResponse with funnel metrics

        Raises:
            HTTPException: 400 if date_from > date_to
            HTTPException: 404 if no data found
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch conversion funnel from repository
        metrics = self.repository.get_conversion_funnel(date_from, date_to)

        if not metrics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No GA4 conversion funnel data found for the specified criteria"
            )

        return self._map_to_response(metrics)

    @staticmethod
    def _map_to_response(data: dict) -> ConversionFunnelResponse:
        """Map database row (uppercase keys) to response model."""
        return ConversionFunnelResponse(
            sessions=int(data.get("SESSIONS") or 0),
            product_views=int(data.get("PRODUCT_VIEWS") or 0),
            add_to_cart=int(data.get("ADD_TO_CART") or 0),
            purchases=int(data.get("PURCHASES") or 0)
        )


# Singleton instance for dependency injection
ga4_conversion_funnel_service = GA4ConversionFunnelService()
