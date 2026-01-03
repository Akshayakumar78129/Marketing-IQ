"""
Traffic Source Attribution service - Business logic layer for traffic source attribution metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import traffic_source_attribution_repository
from .models import TrafficSourceAttributionResponse, TrafficSourceAttribution


class TrafficSourceAttributionService:
    """Service class for traffic source attribution business logic."""

    def __init__(self, repository=traffic_source_attribution_repository):
        self.repository = repository

    def get_traffic_source_attribution(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> TrafficSourceAttributionResponse:
        """
        Get traffic source attribution data grouped by source/medium.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            TrafficSourceAttributionResponse with attribution data

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
        data = self.repository.get_traffic_source_attribution(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list) -> TrafficSourceAttributionResponse:
        """Map database rows to TrafficSourceAttributionResponse."""
        items = [
            TrafficSourceAttribution(
                source_medium=row.get("SOURCE_MEDIUM") or "Unknown",
                sessions=int(row.get("SESSIONS") or 0),
                engaged=int(row.get("ENGAGED") or 0),
                users=int(row.get("USERS") or 0),
                engagement_rate_pct=float(row.get("ENG_RATE_PCT") or 0),
                sessions_per_user=float(row.get("SESS_PER_USER") or 0)
            )
            for row in data
        ]

        total_sessions = sum(item.sessions for item in items)
        total_users = sum(item.users for item in items)

        return TrafficSourceAttributionResponse(
            items=items,
            total_sessions=total_sessions,
            total_users=total_users
        )


# Singleton instance for dependency injection
traffic_source_attribution_service = TrafficSourceAttributionService()
