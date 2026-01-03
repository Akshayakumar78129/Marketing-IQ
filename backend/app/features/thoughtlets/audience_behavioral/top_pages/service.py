"""
Top Pages service - Business logic layer for page metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import top_pages_repository
from .models import TopPagesResponse, PageItem


class TopPagesService:
    """Service class for top pages business logic."""

    def __init__(self, repository=top_pages_repository):
        self.repository = repository

    def get_top_pages(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> TopPagesResponse:
        """
        Get top pages with engagement metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            TopPagesResponse with page metrics

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
        data = self.repository.get_top_pages(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> TopPagesResponse:
        """Map database rows to TopPagesResponse."""
        items = [
            PageItem(
                page_path=row.get("PAGE_PATH") or "/",
                page_type=row.get("PAGE_TYPE") or "Other",
                views=int(row.get("VIEWS") or 0),
                users=int(row.get("USERS") or 0),
                avg_time_seconds=float(row.get("AVG_TIME_SECONDS") or 0),
                views_per_user=float(row.get("VIEWS_PER_USER") or 0)
            )
            for row in data
        ]

        return TopPagesResponse(
            items=items,
            total_pages=len(items)
        )


# Singleton instance for dependency injection
top_pages_service = TopPagesService()
