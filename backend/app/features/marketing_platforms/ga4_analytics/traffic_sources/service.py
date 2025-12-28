"""
GA4 Analytics Traffic Sources service - Business logic layer for traffic sources operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import ga4_traffic_sources_repository
from .models import TrafficSourceItem, TrafficSourcesListResponse


class GA4TrafficSourcesService:
    """Service class for GA4 Analytics traffic sources business logic."""

    def __init__(self, repository=ga4_traffic_sources_repository):
        self.repository = repository

    def get_traffic_sources(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> TrafficSourcesListResponse:
        """
        Get traffic sources with metrics, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            TrafficSourcesListResponse with list of traffic sources

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch traffic sources from repository
        results = self.repository.get_traffic_sources(date_from, date_to)

        # Map database results to response models
        items = [self._map_to_item(row) for row in results]

        return TrafficSourcesListResponse(
            items=items,
            total=len(items)
        )

    @staticmethod
    def _map_to_item(data: dict) -> TrafficSourceItem:
        """Map database row (uppercase keys) to response model."""
        return TrafficSourceItem(
            source=str(data.get("SOURCE") or "(not set)"),
            sessions=int(data.get("SESSIONS") or 0),
            users=int(data.get("USERS") or 0),
            revenue=float(data.get("REVENUE") or 0)
        )


# Singleton instance for dependency injection
ga4_traffic_sources_service = GA4TrafficSourcesService()
