"""
Meta Ads Ad Sets service - Business logic layer for ad set metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status as http_status

from .repository import meta_ads_ad_set_repository
from .models import MetaAdsAdSetResponse, MetaAdsAdSetListResponse


class MetaAdsAdSetService:
    """Service class for Meta Ads ad set business logic."""

    def __init__(self, repository=meta_ads_ad_set_repository):
        self.repository = repository

    def get_ad_sets(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        ad_set_id: Optional[str] = None
    ) -> MetaAdsAdSetListResponse:
        """
        Get Meta Ads ad set metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            ad_set_id: Optional ad set ID filter

        Returns:
            MetaAdsAdSetListResponse with list of ad set metrics

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch ad sets from repository
        ad_sets_data = self.repository.get_ad_sets(date_from, date_to, ad_set_id)

        # Map database results to response models
        ad_sets = [self._map_to_response(row) for row in ad_sets_data]

        return MetaAdsAdSetListResponse(
            ad_sets=ad_sets,
            total_count=len(ad_sets)
        )

    @staticmethod
    def _map_to_response(data: dict) -> MetaAdsAdSetResponse:
        """Map database row (uppercase keys) to response model."""
        return MetaAdsAdSetResponse(
            ad_set_id=str(data.get("AD_SET_ID") or ""),
            ad_set_name=str(data.get("AD_SET_NAME") or ""),
            campaign_name=str(data.get("CAMPAIGN_NAME") or ""),
            spend=float(data.get("TOTAL_SPEND") or 0),
            reach=int(data.get("TOTAL_REACH") or 0),
            clicks=int(data.get("TOTAL_CLICKS") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0),
            impressions=int(data.get("TOTAL_IMPRESSIONS") or 0)
        )


# Singleton instance for dependency injection
meta_ads_ad_set_service = MetaAdsAdSetService()
