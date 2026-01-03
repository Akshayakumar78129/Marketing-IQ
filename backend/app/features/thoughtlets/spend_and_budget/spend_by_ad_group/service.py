"""
Thoughtlets Spend and Budget - Spend by Ad Group service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import spend_by_ad_group_repository
from .models import SpendByAdGroupResponse, AdGroupSpend


class SpendByAdGroupService:
    """Service class for spend by ad group business logic."""

    def __init__(self, repository=spend_by_ad_group_repository):
        self.repository = repository

    def get_spend_by_ad_group(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> SpendByAdGroupResponse:
        """
        Get spend by ad group with optional date filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            SpendByAdGroupResponse with ad group data

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
        data = self.repository.get_spend_by_ad_group(
            date_from=date_from,
            date_to=date_to
        )

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> SpendByAdGroupResponse:
        """Map database rows to SpendByAdGroupResponse."""
        items = []

        for row in data:
            items.append(AdGroupSpend(
                campaign=row.get("CAMPAIGN", "Unknown"),
                impressions=int(row.get("IMPRESSIONS") or 0),
                clicks=int(row.get("CLICKS") or 0),
                spend=float(row.get("SPEND") or 0),
                conversions=float(row.get("CONVERSIONS") or 0),
                roas=float(row.get("ROAS") or 0)
            ))

        return SpendByAdGroupResponse(items=items)


# Singleton instance for dependency injection
spend_by_ad_group_service = SpendByAdGroupService()
