"""
Revenue & Lifetime Value - CAC Metrics service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import cac_metrics_repository
from .models import CACMetricsResponse


class CACMetricsService:
    """Service class for CAC metrics business logic."""

    def __init__(self, repository=cac_metrics_repository):
        self.repository = repository

    def get_cac_metrics(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> CACMetricsResponse:
        """
        Get Customer Acquisition Cost metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            CACMetricsResponse with CAC by platform and spend

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
        data = self.repository.get_cac_metrics(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: dict) -> CACMetricsResponse:
        """Map database row to CACMetricsResponse."""
        return CACMetricsResponse(
            cac_google=float(data.get("CAC_GOOGLE") or 0),
            cac_meta=float(data.get("CAC_META") or 0),
            cac_blended=float(data.get("CAC_BLENDED") or 0),
            google_ads_spend=float(data.get("GOOGLE_ADS_SPEND") or 0),
            meta_ads_spend=float(data.get("META_ADS_SPEND") or 0),
            total_ad_spend=float(data.get("TOTAL_AD_SPEND") or 0)
        )


# Singleton instance for dependency injection
cac_metrics_service = CACMetricsService()
