"""
Traffic by Source service - Business logic layer for traffic source metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import traffic_by_source_repository
from .models import TrafficBySourceResponse, TrafficSourceItem


class TrafficBySourceService:
    """Service class for traffic by source business logic."""

    def __init__(self, repository=traffic_by_source_repository):
        self.repository = repository

    def get_traffic_by_source(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> TrafficBySourceResponse:
        """
        Get session distribution by source/medium.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            TrafficBySourceResponse with traffic source distribution

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
        data = self.repository.get_traffic_by_source(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> TrafficBySourceResponse:
        """Map database rows to TrafficBySourceResponse."""
        items = [
            TrafficSourceItem(
                source_medium=row.get("SOURCE_MEDIUM") or "unknown",
                sessions=int(row.get("SESSIONS") or 0)
            )
            for row in data
        ]

        total_sessions = sum(item.sessions for item in items)

        return TrafficBySourceResponse(
            items=items,
            total_sessions=total_sessions
        )


# Singleton instance for dependency injection
traffic_by_source_service = TrafficBySourceService()
