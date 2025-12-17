"""
Meta Ads Overview service - Business logic layer for overview operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import meta_ads_overview_repository
from .models import MetaAdsOverviewResponse


class MetaAdsOverviewService:
    """Service class for Meta Ads overview business logic."""

    def __init__(self, repository=meta_ads_overview_repository):
        self.repository = repository

    def get_overview(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> MetaAdsOverviewResponse:
        """
        Get Meta Ads overview metrics, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            MetaAdsOverviewResponse with aggregated metrics

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
                detail=f"No Meta Ads data found for date range {date_from} to {date_to}"
            )

        # Map database result (uppercase keys from Snowflake) to response model
        return self._map_to_response(metrics)

    @staticmethod
    def _map_to_response(data: dict) -> MetaAdsOverviewResponse:
        """Map database row (uppercase keys) to response model."""
        return MetaAdsOverviewResponse(
            total_spend=float(data.get("TOTAL_SPEND") or 0),
            impressions=int(data.get("TOTAL_IMPRESSIONS") or 0),
            reach=int(data.get("TOTAL_REACH") or 0),
            clicks=int(data.get("TOTAL_CLICKS") or 0),
            conversions=float(data.get("TOTAL_CONVERSIONS") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0),
            cpm=float(data.get("CPM") or 0),
            roas=float(data.get("ROAS") or 0)
        )


# Singleton instance for dependency injection
meta_ads_overview_service = MetaAdsOverviewService()
