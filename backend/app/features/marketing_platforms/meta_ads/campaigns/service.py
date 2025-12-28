"""
Meta Ads Campaigns service - Business logic layer for campaign operations.
"""
from datetime import date
from typing import Optional, List
from fastapi import HTTPException, status as http_status

from .repository import meta_ads_campaigns_repository
from .models import MetaAdsCampaignResponse, MetaAdsCampaignsListResponse


class MetaAdsCampaignsService:
    """Service class for Meta Ads campaigns business logic."""

    def __init__(self, repository=meta_ads_campaigns_repository):
        self.repository = repository

    def get_campaigns(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        status: Optional[str] = None
    ) -> MetaAdsCampaignsListResponse:
        """
        Get Meta Ads campaigns with metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            status: Optional campaign status filter

        Returns:
            MetaAdsCampaignsListResponse with list of campaigns

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch campaigns from repository
        campaigns_data = self.repository.get_campaigns(date_from, date_to, status)

        # Map database results to response models
        campaigns = [self._map_to_response(row) for row in campaigns_data]

        return MetaAdsCampaignsListResponse(
            campaigns=campaigns,
            total_count=len(campaigns)
        )

    @staticmethod
    def _map_to_response(data: dict) -> MetaAdsCampaignResponse:
        """Map database row (uppercase keys) to response model."""
        return MetaAdsCampaignResponse(
            campaign_id=str(data.get("CAMPAIGN_ID") or ""),
            campaign_name=str(data.get("CAMPAIGN_NAME") or ""),
            status=str(data.get("STATUS") or ""),
            total_spend=float(data.get("TOTAL_SPEND") or 0),
            impressions=int(data.get("TOTAL_IMPRESSIONS") or 0),
            clicks=int(data.get("TOTAL_CLICKS") or 0),
            conversions=float(data.get("TOTAL_CONVERSIONS") or 0),
            revenue=float(data.get("TOTAL_REVENUE") or 0),
            roas=float(data.get("ROAS") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0),
            cpm=float(data.get("CPM") or 0)
        )


# Singleton instance for dependency injection
meta_ads_campaigns_service = MetaAdsCampaignsService()
