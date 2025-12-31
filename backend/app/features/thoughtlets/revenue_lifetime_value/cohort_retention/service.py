"""
Revenue & Lifetime Value - Cohort Retention service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import cohort_retention_repository
from .models import CohortRetentionResponse, CohortRetentionItem


class CohortRetentionService:
    """Service class for cohort retention business logic."""

    def __init__(self, repository=cohort_retention_repository):
        self.repository = repository

    def get_cohort_retention(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 12
    ) -> CohortRetentionResponse:
        """
        Get cohort retention data.

        Args:
            date_from: Optional start date for the cohorts
            date_to: Optional end date for the cohorts
            limit: Number of cohorts to return (default: 12)

        Returns:
            CohortRetentionResponse with list of cohort data

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
        data = self.repository.get_cohort_retention(date_from, date_to, limit)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> CohortRetentionResponse:
        """Map database rows to CohortRetentionResponse."""
        cohorts = [
            CohortRetentionItem(
                cohort_month=row.get("COHORT_MONTH"),
                initial_size=int(row.get("INITIAL_SIZE") or 0),
                months_since=int(row.get("MONTHS_SINCE") or 0),
                active_customers=int(row.get("ACTIVE_CUSTOMERS") or 0),
                retention_rate=float(row.get("RETENTION_RATE") or 0)
            )
            for row in data
        ]
        return CohortRetentionResponse(cohorts=cohorts)


# Singleton instance for dependency injection
cohort_retention_service = CohortRetentionService()
