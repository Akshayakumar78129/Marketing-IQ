"""
Thoughtlets Core Performance ROAS by Platform service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import roas_by_platform_repository
from .models import RoasByPlatformItem, RoasByPlatformResponse


class RoasByPlatformService:
    """Service class for ROAS by platform business logic."""

    def __init__(self, repository=roas_by_platform_repository):
        self.repository = repository

    def get_roas_by_platform(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> RoasByPlatformResponse:
        """
        Get ROAS grouped by platform.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            RoasByPlatformResponse with platform ROAS data

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
        data = self.repository.get_roas_by_platform(date_from, date_to)

        # Map database results to response model
        return RoasByPlatformResponse(
            platforms=[self._map_to_item(row) for row in data]
        )

    @staticmethod
    def _map_to_item(data: dict) -> RoasByPlatformItem:
        """Map database row to RoasByPlatformItem."""
        return RoasByPlatformItem(
            platform=str(data.get("PLATFORM") or "Unknown"),
            roas=float(data.get("ROAS") or 0)
        )


# Singleton instance for dependency injection
roas_by_platform_service = RoasByPlatformService()
