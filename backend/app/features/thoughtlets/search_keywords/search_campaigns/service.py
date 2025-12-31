"""
Search & Keywords - Search Campaigns Performance service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import search_campaigns_repository
from .models import SearchCampaignsResponse, SearchCampaignItem


class SearchCampaignsService:
    """Service class for search campaigns performance business logic."""

    def __init__(self, repository=search_campaigns_repository):
        self.repository = repository

    def get_search_campaigns(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> SearchCampaignsResponse:
        """
        Get search campaign performance metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            SearchCampaignsResponse with list of campaign performance data

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
        data = self.repository.get_search_campaigns(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> SearchCampaignsResponse:
        """Map database rows to SearchCampaignsResponse."""
        campaigns = [
            SearchCampaignItem(
                campaign=str(row.get("CAMPAIGN") or ""),
                type=str(row.get("TYPE") or ""),
                status=str(row.get("STATUS") or ""),
                impressions=int(row.get("IMPRESSIONS") or 0),
                clicks=int(row.get("CLICKS") or 0),
                ctr=float(row.get("CTR") or 0),
                spend=float(row.get("SPEND") or 0),
                conversions=float(row.get("CONVERSIONS") or 0),
                roas=float(row.get("ROAS") or 0)
            )
            for row in data
        ]
        return SearchCampaignsResponse(campaigns=campaigns)


# Singleton instance for dependency injection
search_campaigns_service = SearchCampaignsService()
