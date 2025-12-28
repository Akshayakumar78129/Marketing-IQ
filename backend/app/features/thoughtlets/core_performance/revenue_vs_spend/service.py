"""
Thoughtlets Core Performance Revenue vs Spend service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import revenue_vs_spend_repository
from .models import RevenueVsSpendItem, RevenueVsSpendResponse


class RevenueVsSpendService:
    """Service class for revenue vs spend business logic."""

    def __init__(self, repository=revenue_vs_spend_repository):
        self.repository = repository

    def get_revenue_vs_spend(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> RevenueVsSpendResponse:
        """
        Get monthly revenue vs spend data.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            RevenueVsSpendResponse with monthly data

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
        data = self.repository.get_revenue_vs_spend(date_from, date_to)

        # Map database results to response model
        return RevenueVsSpendResponse(
            data=[self._map_to_item(row) for row in data]
        )

    @staticmethod
    def _map_to_item(data: dict) -> RevenueVsSpendItem:
        """Map database row to RevenueVsSpendItem."""
        return RevenueVsSpendItem(
            month=str(data.get("MONTH") or ""),
            revenue=float(data.get("REVENUE") or 0),
            spend=float(data.get("SPEND") or 0)
        )


# Singleton instance for dependency injection
revenue_vs_spend_service = RevenueVsSpendService()
