"""
Creative & Messaging - Ad Set Performance service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import ad_set_performance_repository
from .models import AdSetPerformanceResponse, AdSetPerformanceItem


class AdSetPerformanceService:
    """Service class for ad set performance business logic."""

    def __init__(self, repository=ad_set_performance_repository):
        self.repository = repository

    def get_ad_set_performance(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> AdSetPerformanceResponse:
        """
        Get ad set performance data for table.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering

        Returns:
            AdSetPerformanceResponse with table data

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
        data = self.repository.get_ad_set_performance(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list) -> AdSetPerformanceResponse:
        """Map database rows to AdSetPerformanceResponse."""
        items = [
            AdSetPerformanceItem(
                ad_set=row.get("AD_SET", "Unknown"),
                campaign=row.get("CAMPAIGN", "Unknown"),
                impressions=int(row.get("IMPRESSIONS") or 0),
                reach=int(row.get("REACH") or 0),
                clicks=int(row.get("CLICKS") or 0),
                ctr=float(row.get("CTR") or 0),
                cpc=float(row.get("CPC")) if row.get("CPC") is not None else None,
                spend=float(row.get("SPEND") or 0)
            )
            for row in data
        ]
        return AdSetPerformanceResponse(data=items)


# Singleton instance for dependency injection
ad_set_performance_service = AdSetPerformanceService()
