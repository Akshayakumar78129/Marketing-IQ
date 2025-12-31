"""
Search & Keywords - Keywords Performance service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import keywords_repository
from .models import KeywordsListResponse, KeywordPerformanceItem


class KeywordsService:
    """Service class for keywords performance business logic."""

    def __init__(self, repository=keywords_repository):
        self.repository = repository

    def get_keywords_performance(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        match_type: Optional[str] = None,
        limit: int = 50
    ) -> KeywordsListResponse:
        """
        Get all keywords with performance metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            match_type: Optional filter by match type
            limit: Number of results to return

        Returns:
            KeywordsListResponse with list of keyword performance data

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
        data = self.repository.get_keywords_performance(date_from, date_to, match_type, limit)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> KeywordsListResponse:
        """Map database rows to KeywordsListResponse."""
        keywords = [
            KeywordPerformanceItem(
                keyword=str(row.get("KEYWORD") or ""),
                match_type=str(row.get("MATCH") or "UNKNOWN"),
                impressions=int(row.get("IMPRESSIONS") or 0),
                clicks=int(row.get("CLICKS") or 0),
                ctr=float(row.get("CTR") or 0),
                cpc=float(row.get("CPC") or 0),
                spend=float(row.get("SPEND") or 0),
                conversions=float(row.get("CONVERSIONS") or 0),
                conv_rate=float(row.get("CONV_RATE") or 0)
            )
            for row in data
        ]
        return KeywordsListResponse(keywords=keywords, total_count=len(keywords))


# Singleton instance for dependency injection
keywords_service = KeywordsService()
