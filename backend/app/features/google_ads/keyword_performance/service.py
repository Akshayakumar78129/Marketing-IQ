"""
Google Ads Keyword Performance service - Business logic layer for keyword performance operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import keyword_performance_repository
from .models import KeywordPerformanceItem, KeywordPerformanceResponse


class KeywordPerformanceService:
    """Service class for Google Ads keyword performance business logic."""

    def __init__(self, repository=keyword_performance_repository):
        self.repository = repository

    def get_keyword_performance(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> KeywordPerformanceResponse:
        """
        Get Google Ads keyword performance metrics with optional date filters.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            KeywordPerformanceResponse with list of keyword metrics

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch metrics from repository
        keywords = self.repository.get_keyword_performance(
            date_from=date_from,
            date_to=date_to
        )

        # Map database results to response model
        items = [self._map_to_item(keyword) for keyword in keywords]

        return KeywordPerformanceResponse(
            items=items,
            total=len(items)
        )

    @staticmethod
    def _map_to_item(data: dict) -> KeywordPerformanceItem:
        """Map database row (uppercase keys) to response model."""
        return KeywordPerformanceItem(
            keyword=str(data.get("KEYWORD") or ""),
            match=str(data.get("MATCH") or ""),
            impressions=int(data.get("IMPRESSIONS") or 0),
            clicks=int(data.get("CLICKS") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0),
            conversions=int(data.get("CONVERSIONS") or 0),
            cost=float(data.get("COST") or 0)
        )


# Singleton instance for dependency injection
keyword_performance_service = KeywordPerformanceService()
