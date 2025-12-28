"""
Thoughtlets Core Performance Overview service - Business logic layer for aggregated metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import core_performance_overview_repository
from .models import CorePerformanceOverviewResponse


class CorePerformanceOverviewService:
    """Service class for core performance overview business logic."""

    def __init__(self, repository=core_performance_overview_repository):
        self.repository = repository

    def get_overview(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> CorePerformanceOverviewResponse:
        """
        Get aggregated core performance metrics across all platforms.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            CorePerformanceOverviewResponse with aggregated metrics

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
    def _map_to_response(data: dict) -> CorePerformanceOverviewResponse:
        """Map database row to CorePerformanceOverviewResponse."""
        return CorePerformanceOverviewResponse(
            conversions=float(data.get("CONVERSIONS") or 0),
            conversion_rate=float(data.get("CONVERSION_RATE") or 0),
            cost_per_conversion=float(data.get("COST_PER_CONVERSION") or 0),
            revenue=float(data.get("REVENUE") or 0),
            roas=float(data.get("ROAS") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0),
            impressions=int(data.get("IMPRESSIONS") or 0)
        )


# Singleton instance for dependency injection
core_performance_overview_service = CorePerformanceOverviewService()
