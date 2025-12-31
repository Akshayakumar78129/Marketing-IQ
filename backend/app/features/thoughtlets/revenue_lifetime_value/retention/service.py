"""
Revenue & Lifetime Value - Retention service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import retention_repository
from .models import RetentionResponse


class RetentionService:
    """Service class for retention business logic."""

    def __init__(self, repository=retention_repository):
        self.repository = repository

    def get_retention(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> RetentionResponse:
        """
        Get retention metrics by period.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            RetentionResponse with retention rates and counts

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
        data = self.repository.get_retention_metrics(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: dict) -> RetentionResponse:
        """Map database row to RetentionResponse."""
        return RetentionResponse(
            retention_30d=float(data.get("RETENTION_30D") or 0),
            retention_60d=float(data.get("RETENTION_60D") or 0),
            retention_90d=float(data.get("RETENTION_90D") or 0),
            retained_30d_count=int(data.get("RETAINED_30D_COUNT") or 0),
            retained_60d_count=int(data.get("RETAINED_60D_COUNT") or 0),
            retained_90d_count=int(data.get("RETAINED_90D_COUNT") or 0)
        )


# Singleton instance for dependency injection
retention_service = RetentionService()
