"""
Thoughtlets Spend and Budget - Spend by Platform service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import spend_by_platform_repository
from .models import SpendByPlatformResponse, PlatformSpend


class SpendByPlatformService:
    """Service class for spend by platform business logic."""

    def __init__(self, repository=spend_by_platform_repository):
        self.repository = repository

    def get_spend_by_platform(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> SpendByPlatformResponse:
        """
        Get spend breakdown by platform.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            SpendByPlatformResponse with platform spend breakdown

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
        data = self.repository.get_spend_by_platform(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> SpendByPlatformResponse:
        """Map database rows to SpendByPlatformResponse."""
        items = []
        total_spend = 0.0

        for row in data:
            platform = row.get("PLATFORM", "Unknown")
            spend = float(row.get("SPEND") or 0)
            items.append(PlatformSpend(platform=platform, spend=spend))
            total_spend += spend

        return SpendByPlatformResponse(
            items=items,
            total_spend=total_spend
        )


# Singleton instance for dependency injection
spend_by_platform_service = SpendByPlatformService()
