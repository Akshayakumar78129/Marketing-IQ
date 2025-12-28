"""
Google Ads Spend by Campaign Type service - Business logic layer for spend breakdown operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import spend_by_campaign_type_repository
from .models import SpendByCampaignTypeItem, SpendByCampaignTypeResponse


class SpendByCampaignTypeService:
    """Service class for Google Ads spend by campaign type business logic."""

    def __init__(self, repository=spend_by_campaign_type_repository):
        self.repository = repository

    def get_spend_by_campaign_type(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> SpendByCampaignTypeResponse:
        """
        Get Google Ads spend breakdown by campaign type with optional date filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            SpendByCampaignTypeResponse with list of spend by campaign type

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
        campaign_types = self.repository.get_spend_by_campaign_type(
            date_from=date_from,
            date_to=date_to
        )

        # Map database results to response model
        items = [self._map_to_item(campaign_type) for campaign_type in campaign_types]

        return SpendByCampaignTypeResponse(
            items=items,
            total=len(items)
        )

    @staticmethod
    def _map_to_item(data: dict) -> SpendByCampaignTypeItem:
        """Map database row (uppercase keys) to response model."""
        return SpendByCampaignTypeItem(
            campaign_type=str(data.get("CAMPAIGN_TYPE") or ""),
            total_spend=float(data.get("TOTAL_SPEND") or 0),
            spend_percentage=float(data.get("SPEND_PERCENTAGE") or 0)
        )


# Singleton instance for dependency injection
spend_by_campaign_type_service = SpendByCampaignTypeService()
