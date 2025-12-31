"""
Search & Keywords Top Keywords service - Business logic layer for top keywords.
"""
from datetime import date
from typing import Optional, Literal
from fastapi import HTTPException, status

from .repository import top_keywords_repository
from .models import TopKeywordsResponse, TopKeywordItem


class TopKeywordsService:
    """Service class for top keywords business logic."""

    def __init__(self, repository=top_keywords_repository):
        self.repository = repository

    def get_top_keywords(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        sort_by: Literal["conversions", "clicks"] = "conversions",
        limit: int = 10
    ) -> TopKeywordsResponse:
        """
        Get top keywords by conversions or clicks.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            sort_by: Sort by 'conversions' or 'clicks'
            limit: Number of results to return

        Returns:
            TopKeywordsResponse with list of top keywords

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
        data = self.repository.get_top_keywords(date_from, date_to, sort_by, limit)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> TopKeywordsResponse:
        """Map database rows to TopKeywordsResponse."""
        keywords = [
            TopKeywordItem(
                keyword=str(row.get("KEYWORD") or ""),
                conversions=float(row.get("CONVERSIONS") or 0),
                clicks=int(row.get("CLICKS") or 0)
            )
            for row in data
        ]
        return TopKeywordsResponse(keywords=keywords)


# Singleton instance for dependency injection
top_keywords_service = TopKeywordsService()
