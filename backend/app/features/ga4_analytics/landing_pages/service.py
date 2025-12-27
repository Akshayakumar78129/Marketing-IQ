"""
GA4 Analytics Landing Pages service - Business logic layer for landing page operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import ga4_landing_pages_repository
from .models import LandingPageItem, LandingPagesResponse


class GA4LandingPagesService:
    """Service class for GA4 Analytics landing pages business logic."""

    def __init__(self, repository=ga4_landing_pages_repository):
        self.repository = repository

    def get_landing_pages(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> LandingPagesResponse:
        """
        Get landing pages by entrances, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            LandingPagesResponse with list of landing pages

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch pages from repository
        pages = self.repository.get_landing_pages(date_from, date_to)

        # Map database results to response models
        return LandingPagesResponse(
            pages=[self._map_to_landing_page_item(row) for row in pages]
        )

    @staticmethod
    def _map_to_landing_page_item(data: dict) -> LandingPageItem:
        """Map database row to LandingPageItem."""
        return LandingPageItem(
            page=str(data.get("PAGE") or "/"),
            entrances=int(data.get("ENTRANCES") or 0),
            bounce_rate=float(data.get("BOUNCE_RATE") or 0),
            sessions=int(data.get("SESSIONS") or 0)
        )


# Singleton instance for dependency injection
ga4_landing_pages_service = GA4LandingPagesService()
