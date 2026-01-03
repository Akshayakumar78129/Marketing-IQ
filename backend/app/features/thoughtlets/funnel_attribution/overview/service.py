"""
Funnel & Attribution Overview service - Business logic layer for funnel/attribution metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import funnel_attribution_overview_repository
from .models import FunnelAttributionOverviewResponse


class FunnelAttributionOverviewService:
    """Service class for funnel and attribution overview business logic."""

    def __init__(self, repository=funnel_attribution_overview_repository):
        self.repository = repository

    def get_overview(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> FunnelAttributionOverviewResponse:
        """
        Get aggregated funnel and attribution metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            FunnelAttributionOverviewResponse with aggregated metrics

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
        data = self.repository.get_overview(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: dict) -> FunnelAttributionOverviewResponse:
        """Map database row to FunnelAttributionOverviewResponse."""
        return FunnelAttributionOverviewResponse(
            total_sessions=int(data.get("TOTAL_SESSIONS") or 0),
            engagement_rate=float(data.get("ENGAGEMENT_RATE") or 0),
            view_to_cart_pct=float(data.get("VIEW_TO_CART_PCT") or 0),
            cart_to_purchase_pct=float(data.get("CART_TO_PURCHASE_PCT") or 0),
            cart_abandon_rate=float(data.get("CART_ABANDON_RATE") or 0),
            total_conversions=int(data.get("TOTAL_CONVERSIONS") or 0),
            utm_coverage_pct=float(data.get("UTM_COVERAGE_PCT") or 0),
            avg_order_value=float(data.get("AVG_ORDER_VALUE") or 0)
        )


# Singleton instance for dependency injection
funnel_attribution_overview_service = FunnelAttributionOverviewService()
