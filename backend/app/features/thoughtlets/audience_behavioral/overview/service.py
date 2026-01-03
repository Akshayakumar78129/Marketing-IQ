"""
Audience & Behavioral Overview service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import audience_behavioral_overview_repository
from .models import AudienceBehavioralOverviewResponse


class AudienceBehavioralOverviewService:
    """Service class for audience and behavioral overview business logic."""

    def __init__(self, repository=audience_behavioral_overview_repository):
        self.repository = repository

    def get_overview(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> AudienceBehavioralOverviewResponse:
        """
        Get audience and behavioral overview metrics with optional date filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            AudienceBehavioralOverviewResponse with aggregated metrics

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
        data = self.repository.get_overview(date_from, date_to)

        # Map database result to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: dict) -> AudienceBehavioralOverviewResponse:
        """Map database row (uppercase keys) to response model."""
        return AudienceBehavioralOverviewResponse(
            total_users=int(data.get("TOTAL_USERS") or 0),
            total_sessions=int(data.get("TOTAL_SESSIONS") or 0),
            new_users=int(data.get("NEW_USERS") or 0),
            returning_users=int(data.get("RETURNING_USERS") or 0),
            engagement_rate=float(data.get("ENGAGEMENT_RATE") or 0),
            bounce_rate=float(data.get("BOUNCE_RATE") or 0),
            sessions_per_user=float(data.get("SESSIONS_PER_USER") or 0),
            conversion_rate=float(data.get("CONVERSION_RATE") or 0)
        )


# Singleton instance for dependency injection
audience_behavioral_overview_service = AudienceBehavioralOverviewService()
