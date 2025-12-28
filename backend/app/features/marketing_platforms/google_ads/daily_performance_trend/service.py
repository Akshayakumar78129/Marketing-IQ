"""
Google Ads Daily Performance Trend service - Business logic layer for daily performance operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import daily_performance_trend_repository
from .models import DailyPerformanceTrendItem, DailyPerformanceTrendResponse


class DailyPerformanceTrendService:
    """Service class for Google Ads daily performance trend business logic."""

    def __init__(self, repository=daily_performance_trend_repository):
        self.repository = repository

    def get_daily_performance_trend(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> DailyPerformanceTrendResponse:
        """
        Get Google Ads daily performance trend by day of week with optional date filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            DailyPerformanceTrendResponse with list of daily performance data

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch metrics from repository
        daily_data = self.repository.get_daily_performance_trend(
            date_from=date_from,
            date_to=date_to
        )

        # Map database results to response model
        items = [self._map_to_item(day) for day in daily_data]

        return DailyPerformanceTrendResponse(
            items=items,
            total=len(items)
        )

    @staticmethod
    def _map_to_item(data: dict) -> DailyPerformanceTrendItem:
        """Map database row (uppercase keys) to response model."""
        return DailyPerformanceTrendItem(
            day_name=str(data.get("DAY_NAME") or ""),
            day_order=int(data.get("DAY_ORDER") or 0),
            total_conversions=float(data.get("TOTAL_CONVERSIONS") or 0),
            total_spend=float(data.get("TOTAL_SPEND") or 0)
        )


# Singleton instance for dependency injection
daily_performance_trend_service = DailyPerformanceTrendService()
