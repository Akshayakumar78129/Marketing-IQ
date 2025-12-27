"""
GA4 Analytics Geographic Performance service - Business logic layer for geographic operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import ga4_geographic_performance_repository
from .models import GeographicPerformanceItem, GeographicPerformanceResponse


class GA4GeographicPerformanceService:
    """Service class for GA4 Analytics geographic performance business logic."""

    def __init__(self, repository=ga4_geographic_performance_repository):
        self.repository = repository

    def get_geographic_performance(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> GeographicPerformanceResponse:
        """
        Get geographic performance by country, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            GeographicPerformanceResponse with list of countries

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
        countries = self.repository.get_geographic_performance(date_from, date_to)

        # Map database results to response models
        return GeographicPerformanceResponse(
            countries=[self._map_to_geographic_item(row) for row in countries]
        )

    @staticmethod
    def _map_to_geographic_item(data: dict) -> GeographicPerformanceItem:
        """Map database row to GeographicPerformanceItem."""
        return GeographicPerformanceItem(
            country=str(data.get("COUNTRY") or "Unknown"),
            sessions=int(data.get("SESSIONS") or 0),
            conv_rate=float(data.get("CONV_RATE") or 0),
            revenue=float(data.get("REVENUE") or 0)
        )


# Singleton instance for dependency injection
ga4_geographic_performance_service = GA4GeographicPerformanceService()
