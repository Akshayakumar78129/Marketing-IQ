"""
Creative & Messaging - Impressions by Campaign service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import impressions_by_campaign_repository
from .models import ImpressionsByCampaignResponse, CampaignImpressionsItem


class ImpressionsByCampaignService:
    """Service class for impressions by campaign business logic."""

    def __init__(self, repository=impressions_by_campaign_repository):
        self.repository = repository

    def get_impressions_by_campaign(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 10
    ) -> ImpressionsByCampaignResponse:
        """
        Get top campaigns by impressions for bar chart.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering
            limit: Maximum number of campaigns to return

        Returns:
            ImpressionsByCampaignResponse with bar chart data

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
        data = self.repository.get_impressions_by_campaign(date_from, date_to, limit)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list) -> ImpressionsByCampaignResponse:
        """Map database rows to ImpressionsByCampaignResponse."""
        items = [
            CampaignImpressionsItem(
                campaign_name=row.get("CAMPAIGN_NAME", "Unknown"),
                impressions=int(row.get("IMPRESSIONS") or 0)
            )
            for row in data
        ]
        return ImpressionsByCampaignResponse(data=items)


# Singleton instance for dependency injection
impressions_by_campaign_service = ImpressionsByCampaignService()
