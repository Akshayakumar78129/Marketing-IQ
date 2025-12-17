"""
Google Ads Campaign Performance service - Business logic layer for campaign performance operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import campaign_performance_repository
from .models import CampaignPerformanceItem, CampaignPerformanceListResponse


class CampaignPerformanceService:
    """Service class for Google Ads campaign performance business logic."""

    def __init__(self, repository=campaign_performance_repository):
        self.repository = repository

    def get_campaign_performance(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        campaign_status: Optional[str] = None
    ) -> CampaignPerformanceListResponse:
        """
        Get Google Ads campaign performance metrics with optional filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            campaign_status: Optional campaign status filter

        Returns:
            CampaignPerformanceListResponse with list of campaign metrics

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
        campaigns = self.repository.get_campaign_performance(
            date_from=date_from,
            date_to=date_to,
            status=campaign_status
        )

        # Map database results to response model
        items = [self._map_to_item(campaign) for campaign in campaigns]

        return CampaignPerformanceListResponse(
            items=items,
            total=len(items)
        )

    @staticmethod
    def _map_to_item(data: dict) -> CampaignPerformanceItem:
        """Map database row (uppercase keys) to response model."""
        return CampaignPerformanceItem(
            campaign=str(data.get("CAMPAIGN") or ""),
            status=str(data.get("STATUS") or ""),
            spend=float(data.get("SPEND") or 0),
            revenue=float(data.get("REVENUE") or 0),
            roas=float(data.get("ROAS") or 0),
            conversions=int(data.get("CONVERSIONS") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0)
        )


# Singleton instance for dependency injection
campaign_performance_service = CampaignPerformanceService()
