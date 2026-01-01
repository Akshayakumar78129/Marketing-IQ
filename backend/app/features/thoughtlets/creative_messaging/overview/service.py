"""
Creative & Messaging - Overview service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import overview_repository
from .models import OverviewResponse


class OverviewService:
    """Service class for creative messaging overview business logic."""

    def __init__(self, repository=overview_repository):
        self.repository = repository

    def get_overview_metrics(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> OverviewResponse:
        """
        Get overview KPI metrics for creatives.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            OverviewResponse with KPI metrics

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
        data = self.repository.get_overview_metrics(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: dict) -> OverviewResponse:
        """Map database row to OverviewResponse."""
        return OverviewResponse(
            total_creatives=int(data.get("TOTAL_CREATIVES") or 0),
            image_creatives=int(data.get("IMAGE_CREATIVES") or 0),
            video_creatives=int(data.get("VIDEO_CREATIVES") or 0),
            avg_ctr=float(data.get("AVG_CTR") or 0),
            avg_cvr=float(data.get("AVG_CVR")) if data.get("AVG_CVR") is not None else None,
            avg_cpc=float(data.get("AVG_CPC") or 0),
            cpm=float(data.get("CPM") or 0),
            overall_roas=float(data.get("OVERALL_ROAS")) if data.get("OVERALL_ROAS") is not None else None
        )


# Singleton instance for dependency injection
overview_service = OverviewService()
