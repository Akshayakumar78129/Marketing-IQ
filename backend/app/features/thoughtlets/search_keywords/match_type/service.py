"""
Search & Keywords Match Type service - Business logic layer for match type metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import match_type_repository
from .models import MatchTypeResponse, MatchTypeItem


class MatchTypeService:
    """Service class for match type business logic."""

    def __init__(self, repository=match_type_repository):
        self.repository = repository

    def get_match_type_distribution(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> MatchTypeResponse:
        """
        Get keyword count and spend distribution by match type.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            MatchTypeResponse with list of match type data

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
        data = self.repository.get_match_type_distribution(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> MatchTypeResponse:
        """Map database rows to MatchTypeResponse."""
        match_types = [
            MatchTypeItem(
                match_type=str(row.get("MATCH_TYPE") or "UNKNOWN"),
                keyword_count=int(row.get("KEYWORD_COUNT") or 0),
                spend=float(row.get("SPEND") or 0)
            )
            for row in data
        ]
        return MatchTypeResponse(match_types=match_types)


# Singleton instance for dependency injection
match_type_service = MatchTypeService()
