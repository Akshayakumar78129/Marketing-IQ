"""
GA4 Analytics Daily Traffic Trend service - Business logic layer for daily traffic operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import ga4_daily_traffic_trend_repository
from .models import DailyTrafficItem, DailyTrafficTrendResponse


class GA4DailyTrafficTrendService:
    """Service class for GA4 Analytics daily traffic trend business logic."""

    def __init__(self, repository=ga4_daily_traffic_trend_repository):
        self.repository = repository

    def get_daily_traffic_trend(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> DailyTrafficTrendResponse:
        """
        Get daily traffic trend with sessions and users, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            DailyTrafficTrendResponse with list of daily data points

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch daily traffic from repository
        results = self.repository.get_daily_traffic(date_from, date_to)

        # Map database results to response models
        items = [self._map_to_item(row) for row in results]

        return DailyTrafficTrendResponse(
            items=items,
            total=len(items)
        )

    @staticmethod
    def _map_to_item(data: dict) -> DailyTrafficItem:
        """Map database row (uppercase keys) to response model."""
        return DailyTrafficItem(
            date=str(data.get("DATE") or ""),
            sessions=int(data.get("SESSIONS") or 0),
            users=int(data.get("USERS") or 0)
        )


# Singleton instance for dependency injection
ga4_daily_traffic_trend_service = GA4DailyTrafficTrendService()
