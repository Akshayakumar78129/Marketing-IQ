"""
GA4 Analytics Top Pages service - Business logic layer for page operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import ga4_top_pages_repository
from .models import TopPageItem, TopPagesResponse


class GA4TopPagesService:
    """Service class for GA4 Analytics top pages business logic."""

    def __init__(self, repository=ga4_top_pages_repository):
        self.repository = repository

    def get_top_pages(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> TopPagesResponse:
        """
        Get top pages by page views, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            TopPagesResponse with list of top pages

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
        pages = self.repository.get_top_pages(date_from, date_to)

        # Map database results to response models
        return TopPagesResponse(
            pages=[self._map_to_page_item(row) for row in pages]
        )

    @staticmethod
    def _map_to_page_item(data: dict) -> TopPageItem:
        """Map database row to TopPageItem."""
        return TopPageItem(
            page=str(data.get("PAGE") or "/"),
            page_views=int(data.get("PAGE_VIEWS") or 0),
            unique_views=int(data.get("UNIQUE_VIEWS") or 0),
            avg_time_seconds=float(data.get("AVG_TIME_SECONDS") or 0),
            bounce_rate=float(data.get("BOUNCE_RATE") or 0)
        )


# Singleton instance for dependency injection
ga4_top_pages_service = GA4TopPagesService()
