"""
Monthly Conversions service - Business logic layer for monthly conversion metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import monthly_conversions_repository
from .models import MonthlyConversionsResponse, MonthlyConversion


class MonthlyConversionsService:
    """Service class for monthly conversions business logic."""

    def __init__(self, repository=monthly_conversions_repository):
        self.repository = repository

    def get_monthly_conversions(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> MonthlyConversionsResponse:
        """
        Get conversions aggregated by month.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            MonthlyConversionsResponse with monthly conversion data

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
        data = self.repository.get_monthly_conversions(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list) -> MonthlyConversionsResponse:
        """Map database rows to MonthlyConversionsResponse."""
        items = [
            MonthlyConversion(
                month=row.get("MONTH") or "Unknown",
                conversions=float(row.get("CONVERSIONS") or 0)
            )
            for row in data
        ]

        total_conversions = sum(item.conversions for item in items)

        return MonthlyConversionsResponse(
            items=items,
            total_conversions=round(total_conversions, 2)
        )


# Singleton instance for dependency injection
monthly_conversions_service = MonthlyConversionsService()
