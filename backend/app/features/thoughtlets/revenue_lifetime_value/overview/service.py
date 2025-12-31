"""
Revenue & Lifetime Value Overview service - Business logic layer for CLV metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import revenue_overview_repository
from .models import RevenueOverviewResponse


class RevenueOverviewService:
    """Service class for revenue overview business logic."""

    def __init__(self, repository=revenue_overview_repository):
        self.repository = repository

    def get_overview(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> RevenueOverviewResponse:
        """
        Get aggregated revenue and CLV metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            RevenueOverviewResponse with aggregated metrics

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch data from repository (two separate queries)
        metrics_data = self.repository.get_metrics_data(date_from, date_to)
        clv_data = self.repository.get_clv_data()

        # Combine and map to response model
        return self._map_to_response(metrics_data, clv_data)

    @staticmethod
    def _map_to_response(metrics_data: dict, clv_data: dict) -> RevenueOverviewResponse:
        """Map database rows to RevenueOverviewResponse."""
        return RevenueOverviewResponse(
            total_revenue=float(metrics_data.get("TOTAL_REVENUE") or 0),
            avg_clv=float(clv_data.get("AVG_CLV") or 0),
            historic_clv=float(clv_data.get("HISTORIC_CLV") or 0),
            predicted_clv=float(clv_data.get("PREDICTED_CLV") or 0),
            repeat_purchase_rate=float(metrics_data.get("REPEAT_PURCHASE_RATE") or 0),
            clv_cac_ratio=float(metrics_data.get("CLV_CAC_RATIO") or 0),
            avg_aov=float(metrics_data.get("AVG_AOV") or 0),
            churn_risk=float(clv_data.get("CHURN_RISK") or 0)
        )


# Singleton instance for dependency injection
revenue_overview_service = RevenueOverviewService()
