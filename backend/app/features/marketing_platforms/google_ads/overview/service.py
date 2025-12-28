"""
Google Ads Overview service - Business logic layer for overview operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import google_ads_overview_repository
from .models import GoogleAdsOverviewResponse


class GoogleAdsOverviewService:
    """Service class for Google Ads overview business logic."""

    def __init__(self, repository=google_ads_overview_repository):
        self.repository = repository

    def get_overview(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> GoogleAdsOverviewResponse:
        """
        Get Google Ads overview metrics, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            GoogleAdsOverviewResponse with aggregated metrics

        Raises:
            HTTPException: 400 if date_from > date_to
            HTTPException: 404 if no data found
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch metrics from repository
        metrics = self.repository.get_overview_metrics(date_from, date_to)

        if not metrics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Google Ads data found for date range {date_from} to {date_to}"
            )

        # Map database result (uppercase keys from Snowflake) to response model
        return self._map_to_response(metrics)

    @staticmethod
    def _map_to_response(data: dict) -> GoogleAdsOverviewResponse:
        """Map database row (uppercase keys) to response model."""
        return GoogleAdsOverviewResponse(
            total_spend=float(data.get("TOTAL_SPEND") or 0),
            total_conversions=float(data.get("TOTAL_CONVERSIONS") or 0),
            total_revenue=float(data.get("TOTAL_REVENUE") or 0),
            roas=float(data.get("ROAS") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0),
            avg_quality_score=float(data["AVG_QUALITY_SCORE"]) if data.get("AVG_QUALITY_SCORE") is not None else None
        )


# Singleton instance for dependency injection
google_ads_overview_service = GoogleAdsOverviewService()
