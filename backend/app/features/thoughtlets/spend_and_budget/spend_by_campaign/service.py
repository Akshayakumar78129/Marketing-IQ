"""
Thoughtlets Spend and Budget - Spend by Campaign service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import spend_by_campaign_repository
from .models import SpendByCampaignResponse, CampaignSpend


class SpendByCampaignService:
    """Service class for spend by campaign business logic."""

    def __init__(self, repository=spend_by_campaign_repository):
        self.repository = repository

    def get_spend_by_campaign(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        platform: Optional[str] = None,
        campaign_status: Optional[str] = None
    ) -> SpendByCampaignResponse:
        """
        Get spend by campaign with filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            platform: Optional platform filter
            campaign_status: Optional status filter

        Returns:
            SpendByCampaignResponse with campaign data

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
        data = self.repository.get_spend_by_campaign(
            date_from=date_from,
            date_to=date_to,
            platform=platform,
            status=campaign_status
        )

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> SpendByCampaignResponse:
        """Map database rows to SpendByCampaignResponse."""
        items = []

        for row in data:
            items.append(CampaignSpend(
                campaign=row.get("CAMPAIGN", "Unknown"),
                platform=row.get("PLATFORM", "Unknown"),
                status=row.get("STATUS", "Unknown"),
                spend=float(row.get("SPEND") or 0),
                revenue=float(row.get("REVENUE") or 0),
                roas=float(row.get("ROAS") or 0),
                conversions=float(row.get("CONVERSIONS") or 0),
                cpc=float(row.get("CPC") or 0)
            ))

        return SpendByCampaignResponse(items=items)


# Singleton instance for dependency injection
spend_by_campaign_service = SpendByCampaignService()
