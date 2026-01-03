"""
Meta Ads Funnel service - Business logic layer for Meta pixel conversion events.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import meta_ads_funnel_repository
from .models import MetaAdsFunnelResponse


class MetaAdsFunnelService:
    """Service class for Meta Ads funnel business logic."""

    def __init__(self, repository=meta_ads_funnel_repository):
        self.repository = repository

    def get_funnel(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> MetaAdsFunnelResponse:
        """
        Get Meta Ads funnel metrics (pixel conversion events).

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            MetaAdsFunnelResponse with funnel metrics

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
    def _map_to_response(data: dict) -> MetaAdsFunnelResponse:
        """Map database row to MetaAdsFunnelResponse."""
        return MetaAdsFunnelResponse(
            view_content=int(data.get("VIEW_CONTENT") or 0),
            add_to_cart=int(data.get("ADD_TO_CART") or 0),
            initiate_checkout=int(data.get("INITIATE_CHECKOUT") or 0),
            purchase=int(data.get("PURCHASE") or 0)
        )


# Singleton instance for dependency injection
meta_ads_funnel_service = MetaAdsFunnelService()
