"""
Engagement Funnel service - Business logic layer for engagement funnel metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import engagement_funnel_repository
from .models import EngagementFunnelResponse


class EngagementFunnelService:
    """Service class for engagement funnel business logic."""

    def __init__(self, repository=engagement_funnel_repository):
        self.repository = repository

    def get_engagement_funnel(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> EngagementFunnelResponse:
        """
        Get engagement funnel metrics (users -> sessions -> engaged -> conversions).

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            EngagementFunnelResponse with funnel metrics

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
        data = self.repository.get_engagement_funnel(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: dict) -> EngagementFunnelResponse:
        """Map database row to EngagementFunnelResponse."""
        # Handle NaN/None values from conversions
        conversions = data.get("TOTAL_CONVERSIONS")
        if conversions is None or (isinstance(conversions, float) and conversions != conversions):
            conversions = 0

        return EngagementFunnelResponse(
            total_users=int(data.get("TOTAL_USERS") or 0),
            sessions=int(data.get("TOTAL_SESSIONS") or 0),
            engaged=int(data.get("ENGAGED_SESSIONS") or 0),
            conversions=int(conversions)
        )


# Singleton instance for dependency injection
engagement_funnel_service = EngagementFunnelService()
