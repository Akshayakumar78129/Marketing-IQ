"""
Creative & Messaging - CTA Types service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import cta_types_repository
from .models import CTATypesResponse, CTATypeItem


class CTATypesService:
    """Service class for CTA types business logic."""

    def __init__(self, repository=cta_types_repository):
        self.repository = repository

    def get_cta_types(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> CTATypesResponse:
        """
        Get CTA type distribution for bar chart.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering

        Returns:
            CTATypesResponse with bar chart data

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
        data = self.repository.get_cta_types(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list) -> CTATypesResponse:
        """Map database rows to CTATypesResponse."""
        items = [
            CTATypeItem(
                cta_type=row.get("CTA_TYPE", "UNKNOWN"),
                count=int(row.get("COUNT") or 0)
            )
            for row in data
        ]
        return CTATypesResponse(data=items)


# Singleton instance for dependency injection
cta_types_service = CTATypesService()
