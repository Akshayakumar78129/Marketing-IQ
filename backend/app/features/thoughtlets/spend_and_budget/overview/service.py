"""
Thoughtlets Spend and Budget Overview service - Business logic layer for spend/budget metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import spend_and_budget_overview_repository
from .models import SpendAndBudgetOverviewResponse


class SpendAndBudgetOverviewService:
    """Service class for spend and budget overview business logic."""

    def __init__(self, repository=spend_and_budget_overview_repository):
        self.repository = repository

    def get_overview(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> SpendAndBudgetOverviewResponse:
        """
        Get aggregated spend and budget metrics across all platforms.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            SpendAndBudgetOverviewResponse with aggregated metrics

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
        data = self.repository.get_overview(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: dict) -> SpendAndBudgetOverviewResponse:
        """Map database row to SpendAndBudgetOverviewResponse."""
        return SpendAndBudgetOverviewResponse(
            total_spend=float(data.get("TOTAL_SPEND") or 0),
            total_revenue=float(data.get("TOTAL_REVENUE") or 0),
            overall_roas=float(data.get("OVERALL_ROAS") or 0),
            cost_per_conversion=float(data.get("COST_PER_CONVERSION") or 0),
            avg_cpc=float(data.get("AVG_CPC") or 0),
            avg_daily_spend=float(data.get("AVG_DAILY_SPEND") or 0),
            total_impressions=int(data.get("TOTAL_IMPRESSIONS") or 0),
            conversions=int(data.get("CONVERSIONS") or 0)
        )


# Singleton instance for dependency injection
spend_and_budget_overview_service = SpendAndBudgetOverviewService()
