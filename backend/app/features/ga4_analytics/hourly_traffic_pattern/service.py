"""
GA4 Analytics Hourly Traffic Pattern service - Business logic layer for hourly traffic operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import ga4_hourly_traffic_pattern_repository
from .models import HourlyTrafficItem, HourlyTrafficPatternResponse


class GA4HourlyTrafficPatternService:
    """Service class for GA4 Analytics hourly traffic pattern business logic."""

    def __init__(self, repository=ga4_hourly_traffic_pattern_repository):
        self.repository = repository

    def get_hourly_traffic_pattern(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> HourlyTrafficPatternResponse:
        """
        Get hourly traffic pattern with impressions and clicks, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            HourlyTrafficPatternResponse with list of hourly data points

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch hourly traffic from repository
        results = self.repository.get_hourly_traffic(date_from, date_to)

        # Map database results to response models
        items = [self._map_to_item(row) for row in results]

        return HourlyTrafficPatternResponse(
            items=items,
            total=len(items)
        )

    @staticmethod
    def _map_to_item(data: dict) -> HourlyTrafficItem:
        """Map database row (uppercase keys) to response model."""
        return HourlyTrafficItem(
            hour=int(data.get("HOUR") or 0),
            hour_label=str(data.get("HOUR_LABEL") or ""),
            impressions=int(data.get("IMPRESSIONS") or 0),
            clicks=int(data.get("CLICKS") or 0)
        )


# Singleton instance for dependency injection
ga4_hourly_traffic_pattern_service = GA4HourlyTrafficPatternService()
