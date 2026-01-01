"""
Creative & Messaging - Creative Type Distribution service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import creative_type_distribution_repository
from .models import CreativeTypeDistributionResponse, CreativeTypeItem


class CreativeTypeDistributionService:
    """Service class for creative type distribution business logic."""

    def __init__(self, repository=creative_type_distribution_repository):
        self.repository = repository

    def get_creative_type_distribution(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> CreativeTypeDistributionResponse:
        """
        Get creative type distribution for pie chart.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering

        Returns:
            CreativeTypeDistributionResponse with pie chart data

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
        data = self.repository.get_creative_type_distribution(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list) -> CreativeTypeDistributionResponse:
        """Map database rows to CreativeTypeDistributionResponse."""
        items = [
            CreativeTypeItem(
                creative_type=row.get("CREATIVE_TYPE", "unknown"),
                count=int(row.get("COUNT") or 0)
            )
            for row in data
        ]
        return CreativeTypeDistributionResponse(data=items)


# Singleton instance for dependency injection
creative_type_distribution_service = CreativeTypeDistributionService()
