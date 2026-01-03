"""
eCommerce Funnel service - Business logic layer for eCommerce funnel metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import ecommerce_funnel_repository
from .models import EcommerceFunnelResponse


class EcommerceFunnelService:
    """Service class for eCommerce funnel business logic."""

    def __init__(self, repository=ecommerce_funnel_repository):
        self.repository = repository

    def get_funnel(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> EcommerceFunnelResponse:
        """
        Get eCommerce funnel metrics (View → Cart → Purchase journey).

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            EcommerceFunnelResponse with funnel metrics

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch data from repository
        data = self.repository.get_funnel_metrics(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: dict) -> EcommerceFunnelResponse:
        """Map database row to EcommerceFunnelResponse."""
        return EcommerceFunnelResponse(
            views=int(data.get("VIEWS") or 0),
            add_to_cart=int(data.get("ADD_TO_CART") or 0),
            purchase=int(data.get("PURCHASE") or 0)
        )


# Singleton instance for dependency injection
ecommerce_funnel_service = EcommerceFunnelService()
