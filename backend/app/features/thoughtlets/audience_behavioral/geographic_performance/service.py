"""
Geographic Performance service - Business logic layer for geo performance metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import geographic_performance_repository
from .models import GeographicPerformanceResponse, GeoPerformanceItem


class GeographicPerformanceService:
    """Service class for geographic performance business logic."""

    def __init__(self, repository=geographic_performance_repository):
        self.repository = repository

    def get_geographic_performance(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> GeographicPerformanceResponse:
        """
        Get geographic performance metrics by country.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            GeographicPerformanceResponse with country performance metrics

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
        data = self.repository.get_geographic_performance(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> GeographicPerformanceResponse:
        """Map database rows to GeographicPerformanceResponse."""
        items = [
            GeoPerformanceItem(
                country=row.get("COUNTRY") or "(not set)",
                users=int(row.get("USERS") or 0),
                new_users=int(row.get("NEW_USERS") or 0),
                new_user_pct=float(row.get("NEW_USER_PCT") or 0),
                engaged=int(row.get("ENGAGED") or 0),
                eng_rate_pct=float(row.get("ENG_RATE_PCT") or 0)
            )
            for row in data
        ]

        return GeographicPerformanceResponse(
            items=items,
            total_countries=len(items)
        )


# Singleton instance for dependency injection
geographic_performance_service = GeographicPerformanceService()
