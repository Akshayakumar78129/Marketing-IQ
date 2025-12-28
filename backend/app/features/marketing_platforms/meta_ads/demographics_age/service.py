"""
Meta Ads Demographics Age service - Business logic layer for age demographic metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import meta_ads_demographics_age_repository
from .models import MetaAdsDemographicsAgeResponse, MetaAdsDemographicsAgeListResponse


class MetaAdsDemographicsAgeService:
    """Service class for Meta Ads age demographics business logic."""

    def __init__(self, repository=meta_ads_demographics_age_repository):
        self.repository = repository

    def get_demographics_age(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        age_bracket: Optional[str] = None
    ) -> MetaAdsDemographicsAgeListResponse:
        """
        Get Meta Ads age demographic metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            age_bracket: Optional age bracket filter

        Returns:
            MetaAdsDemographicsAgeListResponse with list of age demographics

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch demographics from repository
        demographics_data = self.repository.get_demographics_age(date_from, date_to, age_bracket)

        # Map database results to response models
        demographics = [self._map_to_response(row) for row in demographics_data]

        return MetaAdsDemographicsAgeListResponse(
            demographics=demographics,
            total_count=len(demographics)
        )

    @staticmethod
    def _map_to_response(data: dict) -> MetaAdsDemographicsAgeResponse:
        """Map database row (uppercase keys) to response model."""
        return MetaAdsDemographicsAgeResponse(
            age_bracket=str(data.get("AGE_BRACKET") or ""),
            impressions=int(data.get("TOTAL_IMPRESSIONS") or 0),
            spend=float(data.get("TOTAL_SPEND") or 0),
            clicks=int(data.get("TOTAL_CLICKS") or 0),
            reach=int(data.get("TOTAL_REACH") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0)
        )


# Singleton instance for dependency injection
meta_ads_demographics_age_service = MetaAdsDemographicsAgeService()
