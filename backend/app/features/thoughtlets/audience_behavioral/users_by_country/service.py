"""
Users by Country service - Business logic layer for country metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import users_by_country_repository
from .models import UsersByCountryResponse, CountryItem


class UsersByCountryService:
    """Service class for users by country business logic."""

    def __init__(self, repository=users_by_country_repository):
        self.repository = repository

    def get_users_by_country(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> UsersByCountryResponse:
        """
        Get user counts by country.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            UsersByCountryResponse with country distribution

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
        data = self.repository.get_users_by_country(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> UsersByCountryResponse:
        """Map database rows to UsersByCountryResponse."""
        items = [
            CountryItem(
                country=row.get("COUNTRY") or "(not set)",
                users=int(row.get("USERS") or 0)
            )
            for row in data
        ]

        total_users = sum(item.users for item in items)

        return UsersByCountryResponse(
            items=items,
            total_users=total_users
        )


# Singleton instance for dependency injection
users_by_country_service = UsersByCountryService()
