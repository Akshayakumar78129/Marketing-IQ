"""
Creative & Messaging - Creatives service - Business logic layer.
"""
import math
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import creatives_repository
from .models import CreativesResponse, CreativeItem


class CreativesService:
    """Service class for creatives business logic."""

    def __init__(self, repository=creatives_repository):
        self.repository = repository

    def get_creatives(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        page: int = 1,
        page_size: int = 10
    ) -> CreativesResponse:
        """
        Get paginated creatives with performance data.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            CreativesResponse with paginated data

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
        data, total = self.repository.get_creatives(date_from, date_to, page, page_size)

        # Calculate total pages
        total_pages = math.ceil(total / page_size) if total > 0 else 0

        # Map database results to response model
        return self._map_to_response(data, total, page, page_size, total_pages)

    @staticmethod
    def _map_to_response(
        data: list,
        total: int,
        page: int,
        page_size: int,
        total_pages: int
    ) -> CreativesResponse:
        """Map database rows to CreativesResponse."""
        items = [
            CreativeItem(
                creative_name=row.get("CREATIVE_NAME", "Unknown"),
                type=row.get("TYPE", "UNKNOWN"),
                headline=row.get("HEADLINE"),
                ctr=float(row.get("CTR") or 0),
                impressions=int(row.get("IMPRESSIONS") or 0),
                primary_text=row.get("PRIMARY_TEXT"),
                status=row.get("STATUS", "UNKNOWN")
            )
            for row in data
        ]
        return CreativesResponse(
            data=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )


# Singleton instance for dependency injection
creatives_service = CreativesService()
