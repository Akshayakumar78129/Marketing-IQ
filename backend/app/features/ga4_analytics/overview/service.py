"""
GA4 Analytics Overview service - Business logic layer for overview operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import ga4_overview_repository
from .models import GA4OverviewResponse


class GA4OverviewService:
    """Service class for GA4 Analytics overview business logic."""

    def __init__(self, repository=ga4_overview_repository):
        self.repository = repository

    def get_overview(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> GA4OverviewResponse:
        """
        Get GA4 Analytics overview metrics, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            GA4OverviewResponse with aggregated metrics

        Raises:
            HTTPException: 400 if date_from > date_to
            HTTPException: 404 if no data found
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch metrics from repository
        metrics = self.repository.get_overview_metrics(date_from, date_to)

        if not metrics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No GA4 Analytics data found for date range {date_from} to {date_to}"
            )

        # Map database result (uppercase keys from Snowflake) to response model
        return self._map_to_response(metrics)

    @staticmethod
    def _map_to_response(data: dict) -> GA4OverviewResponse:
        """Map database row (uppercase keys) to response model."""
        return GA4OverviewResponse(
            sessions=int(data.get("SESSIONS") or 0),
            users=int(data.get("USERS") or 0),
            engaged_sessions=int(data.get("ENGAGED_SESSIONS") or 0),
            engagement_rate=float(data.get("ENGAGEMENT_RATE") or 0),
            sessions_per_user=float(data.get("SESSIONS_PER_USER") or 0),
            conversions=float(data.get("CONVERSIONS") or 0),
            revenue=float(data.get("REVENUE") or 0),
            conversion_value=float(data["CONVERSION_VALUE"]) if data.get("CONVERSION_VALUE") is not None else None
        )


# Singleton instance for dependency injection
ga4_overview_service = GA4OverviewService()
