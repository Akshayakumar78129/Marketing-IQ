"""
Google Ads Ad Group Performance service - Business logic layer for ad group performance operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import ad_group_performance_repository
from .models import AdGroupPerformanceItem, AdGroupPerformanceResponse


class AdGroupPerformanceService:
    """Service class for Google Ads ad group performance business logic."""

    def __init__(self, repository=ad_group_performance_repository):
        self.repository = repository

    def get_ad_group_performance(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> AdGroupPerformanceResponse:
        """
        Get Google Ads ad group performance metrics with optional date filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            AdGroupPerformanceResponse with list of ad group metrics

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch metrics from repository
        ad_groups = self.repository.get_ad_group_performance(
            date_from=date_from,
            date_to=date_to
        )

        # Map database results to response model
        items = [self._map_to_item(ad_group) for ad_group in ad_groups]

        return AdGroupPerformanceResponse(
            items=items,
            total=len(items)
        )

    @staticmethod
    def _map_to_item(data: dict) -> AdGroupPerformanceItem:
        """Map database row (uppercase keys) to response model."""
        return AdGroupPerformanceItem(
            ad_group=str(data.get("AD_GROUP") or ""),
            campaign=str(data.get("CAMPAIGN") or ""),
            impressions=int(data.get("IMPRESSIONS") or 0),
            clicks=int(data.get("CLICKS") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0),
            conversions=int(data.get("CONVERSIONS") or 0),
            cvr=float(data.get("CVR") or 0)
        )


# Singleton instance for dependency injection
ad_group_performance_service = AdGroupPerformanceService()
