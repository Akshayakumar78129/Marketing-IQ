"""
Revenue & Lifetime Value - Churn Distribution service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import churn_distribution_repository
from .models import ChurnDistributionResponse, ChurnDistributionItem


class ChurnDistributionService:
    """Service class for churn distribution business logic."""

    def __init__(self, repository=churn_distribution_repository):
        self.repository = repository

    def get_churn_distribution(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> ChurnDistributionResponse:
        """
        Get churn risk distribution.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering

        Returns:
            ChurnDistributionResponse with list of risk levels and customer counts

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
        data = self.repository.get_churn_distribution(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> ChurnDistributionResponse:
        """Map database rows to ChurnDistributionResponse."""
        distribution = [
            ChurnDistributionItem(
                risk_level=str(row.get("RISK_LEVEL") or ""),
                customer_count=int(row.get("CUSTOMER_COUNT") or 0)
            )
            for row in data
        ]
        return ChurnDistributionResponse(distribution=distribution)


# Singleton instance for dependency injection
churn_distribution_service = ChurnDistributionService()
