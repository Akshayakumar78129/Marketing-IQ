"""
Thoughtlets Core Performance Conversions Trend service - Business logic layer for monthly conversions.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import conversions_trend_repository
from .models import ConversionsTrendItem, ConversionsTrendResponse


class ConversionsTrendService:
    """Service class for conversions trend business logic."""

    def __init__(self, repository=conversions_trend_repository):
        self.repository = repository

    def get_conversions_trend(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> ConversionsTrendResponse:
        """
        Get monthly conversions trend across all platforms.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            ConversionsTrendResponse with monthly conversion data

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
        data = self.repository.get_conversions_trend(date_from, date_to)

        # Map database results to response model
        return ConversionsTrendResponse(
            trend=[self._map_to_trend_item(row) for row in data]
        )

    @staticmethod
    def _map_to_trend_item(data: dict) -> ConversionsTrendItem:
        """Map database row to ConversionsTrendItem."""
        return ConversionsTrendItem(
            month=str(data.get("MONTH") or ""),
            conversions=float(data.get("CONVERSIONS") or 0)
        )


# Singleton instance for dependency injection
conversions_trend_service = ConversionsTrendService()
