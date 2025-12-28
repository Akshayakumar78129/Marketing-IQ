"""
Meta Ads Placements service - Business logic layer for placement metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import meta_ads_placements_repository
from .models import MetaAdsPlacementResponse, MetaAdsPlacementsListResponse


class MetaAdsPlacementsService:
    """Service class for Meta Ads placements business logic."""

    def __init__(self, repository=meta_ads_placements_repository):
        self.repository = repository

    def get_placements(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        placement: Optional[str] = None
    ) -> MetaAdsPlacementsListResponse:
        """
        Get Meta Ads placement metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            placement: Optional placement filter

        Returns:
            MetaAdsPlacementsListResponse with list of placements

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch placements from repository
        placements_data = self.repository.get_placements(date_from, date_to, placement)

        # Map database results to response models
        placements = [self._map_to_response(row) for row in placements_data]

        return MetaAdsPlacementsListResponse(
            placements=placements,
            total_count=len(placements)
        )

    @staticmethod
    def _map_to_response(data: dict) -> MetaAdsPlacementResponse:
        """Map database row (uppercase keys) to response model."""
        return MetaAdsPlacementResponse(
            placement=str(data.get("PLACEMENT") or ""),
            impressions=int(data.get("TOTAL_IMPRESSIONS") or 0),
            reach=int(data.get("TOTAL_REACH") or 0),
            spend=float(data.get("TOTAL_SPEND") or 0),
            clicks=int(data.get("TOTAL_CLICKS") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0)
        )


# Singleton instance for dependency injection
meta_ads_placements_service = MetaAdsPlacementsService()
