"""
Meta Ads Daily Performance service - Business logic layer for daily metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import meta_ads_daily_performance_repository
from .models import MetaAdsDailyPerformanceResponse, MetaAdsDailyPerformanceListResponse


class MetaAdsDailyPerformanceService:
    """Service class for Meta Ads daily performance business logic."""

    def __init__(self, repository=meta_ads_daily_performance_repository):
        self.repository = repository

    def get_daily_performance(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        campaign_id: Optional[str] = None
    ) -> MetaAdsDailyPerformanceListResponse:
        """
        Get Meta Ads daily performance metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            campaign_id: Optional campaign ID filter

        Returns:
            MetaAdsDailyPerformanceListResponse with list of daily metrics

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch daily performance from repository
        daily_data = self.repository.get_daily_performance(date_from, date_to, campaign_id)

        # Map database results to response models
        daily_performance = [self._map_to_response(row) for row in daily_data]

        return MetaAdsDailyPerformanceListResponse(
            daily_performance=daily_performance,
            total_days=len(daily_performance)
        )

    @staticmethod
    def _map_to_response(data: dict) -> MetaAdsDailyPerformanceResponse:
        """Map database row (uppercase keys) to response model."""
        return MetaAdsDailyPerformanceResponse(
            date=data.get("DATE_DAY"),
            spend=float(data.get("DAILY_SPEND") or 0),
            impressions=int(data.get("DAILY_IMPRESSIONS") or 0),
            clicks=int(data.get("DAILY_CLICKS") or 0),
            conversions=float(data.get("DAILY_CONVERSIONS") or 0),
            revenue=float(data.get("DAILY_REVENUE") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0)
        )


# Singleton instance for dependency injection
meta_ads_daily_performance_service = MetaAdsDailyPerformanceService()
