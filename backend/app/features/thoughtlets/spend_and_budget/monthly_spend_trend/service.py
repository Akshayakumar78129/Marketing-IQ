"""
Thoughtlets Spend and Budget - Monthly Spend Trend service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import monthly_spend_trend_repository
from .models import MonthlySpendTrendResponse, MonthlySpend


class MonthlySpendTrendService:
    """Service class for monthly spend trend business logic."""

    def __init__(self, repository=monthly_spend_trend_repository):
        self.repository = repository

    def get_monthly_spend_trend(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> MonthlySpendTrendResponse:
        """
        Get monthly spend trend data.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            MonthlySpendTrendResponse with monthly spend data points

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
        data = self.repository.get_monthly_spend_trend(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> MonthlySpendTrendResponse:
        """Map database rows to MonthlySpendTrendResponse."""
        items = []

        for row in data:
            month = row.get("MONTH", "")
            spend = float(row.get("SPEND") or 0)
            items.append(MonthlySpend(month=month, spend=spend))

        return MonthlySpendTrendResponse(items=items)


# Singleton instance for dependency injection
monthly_spend_trend_service = MonthlySpendTrendService()
