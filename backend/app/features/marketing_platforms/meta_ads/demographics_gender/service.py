"""
Meta Ads Demographics Gender service - Business logic layer for gender demographic metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import meta_ads_demographics_gender_repository
from .models import MetaAdsDemographicsGenderResponse, MetaAdsDemographicsGenderListResponse


class MetaAdsDemographicsGenderService:
    """Service class for Meta Ads gender demographics business logic."""

    def __init__(self, repository=meta_ads_demographics_gender_repository):
        self.repository = repository

    def get_demographics_gender(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        gender: Optional[str] = None
    ) -> MetaAdsDemographicsGenderListResponse:
        """
        Get Meta Ads gender demographic metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            gender: Optional gender filter

        Returns:
            MetaAdsDemographicsGenderListResponse with list of gender demographics

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
        demographics_data = self.repository.get_demographics_gender(date_from, date_to, gender)

        # Map database results to response models
        demographics = [self._map_to_response(row) for row in demographics_data]

        return MetaAdsDemographicsGenderListResponse(
            demographics=demographics,
            total_count=len(demographics)
        )

    @staticmethod
    def _map_to_response(data: dict) -> MetaAdsDemographicsGenderResponse:
        """Map database row (uppercase keys) to response model."""
        return MetaAdsDemographicsGenderResponse(
            gender=str(data.get("GENDER") or ""),
            impressions=int(data.get("TOTAL_IMPRESSIONS") or 0),
            spend=float(data.get("TOTAL_SPEND") or 0),
            clicks=int(data.get("TOTAL_CLICKS") or 0),
            reach=int(data.get("TOTAL_REACH") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0)
        )


# Singleton instance for dependency injection
meta_ads_demographics_gender_service = MetaAdsDemographicsGenderService()
