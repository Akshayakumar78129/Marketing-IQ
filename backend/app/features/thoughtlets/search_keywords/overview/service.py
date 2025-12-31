"""
Search & Keywords Overview service - Business logic layer for keyword metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import search_keywords_overview_repository
from .models import SearchKeywordsOverviewResponse


class SearchKeywordsOverviewService:
    """Service class for search keywords overview business logic."""

    def __init__(self, repository=search_keywords_overview_repository):
        self.repository = repository

    def get_overview(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> SearchKeywordsOverviewResponse:
        """
        Get aggregated keyword performance metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            SearchKeywordsOverviewResponse with aggregated metrics

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
        data = self.repository.get_overview(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: dict) -> SearchKeywordsOverviewResponse:
        """Map database row to SearchKeywordsOverviewResponse."""
        return SearchKeywordsOverviewResponse(
            total_keywords=int(data.get("TOTAL_KEYWORDS") or 0),
            exact_match=int(data.get("EXACT_MATCH") or 0),
            phrase_match=int(data.get("PHRASE_MATCH") or 0),
            broad_match=int(data.get("BROAD_MATCH") or 0),
            avg_ctr=float(data.get("AVG_CTR") or 0),
            avg_cpc=float(data.get("AVG_CPC") or 0),
            conversions=float(data.get("CONVERSIONS") or 0),
            total_spend=float(data.get("TOTAL_SPEND") or 0)
        )


# Singleton instance for dependency injection
search_keywords_overview_service = SearchKeywordsOverviewService()
