"""
Creative & Messaging - CTR by Campaign service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import ctr_by_campaign_repository
from .models import CTRByCampaignResponse, CampaignCTRItem


class CTRByCampaignService:
    """Service class for CTR by campaign business logic."""

    def __init__(self, repository=ctr_by_campaign_repository):
        self.repository = repository

    def get_ctr_by_campaign(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 10
    ) -> CTRByCampaignResponse:
        """
        Get top campaigns by CTR for bar chart.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering
            limit: Maximum number of campaigns to return

        Returns:
            CTRByCampaignResponse with bar chart data

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
        data = self.repository.get_ctr_by_campaign(date_from, date_to, limit)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list) -> CTRByCampaignResponse:
        """Map database rows to CTRByCampaignResponse."""
        items = [
            CampaignCTRItem(
                campaign_name=row.get("CAMPAIGN_NAME", "Unknown"),
                ctr=float(row.get("CTR") or 0)
            )
            for row in data
        ]
        return CTRByCampaignResponse(data=items)


# Singleton instance for dependency injection
ctr_by_campaign_service = CTRByCampaignService()
