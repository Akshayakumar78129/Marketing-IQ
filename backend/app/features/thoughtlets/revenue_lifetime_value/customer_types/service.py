"""
Revenue & Lifetime Value - Customer Types service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import customer_types_repository
from .models import CustomerTypesResponse


class CustomerTypesService:
    """Service class for customer types business logic."""

    def __init__(self, repository=customer_types_repository):
        self.repository = repository

    def get_customer_types(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> CustomerTypesResponse:
        """
        Get customer type distribution.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            CustomerTypesResponse with customer type counts

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
        data = self.repository.get_customer_types(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: dict) -> CustomerTypesResponse:
        """Map database row to CustomerTypesResponse."""
        return CustomerTypesResponse(
            new_customers=int(data.get("NEW_CUSTOMERS") or 0),
            repeat_customers=int(data.get("REPEAT_CUSTOMERS") or 0),
            one_time_customers=int(data.get("ONE_TIME_CUSTOMERS") or 0)
        )


# Singleton instance for dependency injection
customer_types_service = CustomerTypesService()
