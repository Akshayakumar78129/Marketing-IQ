"""
Meta Ads Ad Creatives service - Business logic layer for ad creative metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status as http_status

from .repository import meta_ads_creative_repository
from .models import MetaAdsCreativeResponse, MetaAdsCreativeListResponse


class MetaAdsCreativeService:
    """Service class for Meta Ads creative business logic."""

    def __init__(self, repository=meta_ads_creative_repository):
        self.repository = repository

    def get_creatives(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        ad_id: Optional[str] = None
    ) -> MetaAdsCreativeListResponse:
        """
        Get Meta Ads creative metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            ad_id: Optional ad ID filter

        Returns:
            MetaAdsCreativeListResponse with list of creative metrics

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch creatives from repository
        creatives_data = self.repository.get_creatives(date_from, date_to, ad_id)

        # Map database results to response models
        creatives = [self._map_to_response(row) for row in creatives_data]

        return MetaAdsCreativeListResponse(
            creatives=creatives,
            total_count=len(creatives)
        )

    @staticmethod
    def _map_to_response(data: dict) -> MetaAdsCreativeResponse:
        """Map database row (uppercase keys) to response model."""
        return MetaAdsCreativeResponse(
            ad_id=str(data.get("AD_ID") or ""),
            ad_name=str(data.get("AD_NAME") or ""),
            ad_type=data.get("AD_TYPE"),
            spend=float(data.get("TOTAL_SPEND") or 0),
            impressions=int(data.get("TOTAL_IMPRESSIONS") or 0),
            clicks=int(data.get("TOTAL_CLICKS") or 0),
            conversions=float(data.get("TOTAL_CONVERSIONS") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0)
        )


# Singleton instance for dependency injection
meta_ads_creative_service = MetaAdsCreativeService()
