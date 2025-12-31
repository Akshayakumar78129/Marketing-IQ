"""
Revenue & Lifetime Value - Customer Segments service - Business logic layer.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import customer_segments_repository
from .models import CustomerSegmentsResponse, CustomerSegmentItem


class CustomerSegmentsService:
    """Service class for customer segments business logic."""

    def __init__(self, repository=customer_segments_repository):
        self.repository = repository

    def get_customer_segments(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> CustomerSegmentsResponse:
        """
        Get customer distribution by CLV segment.

        Args:
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering

        Returns:
            CustomerSegmentsResponse with list of segments and customer counts

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
        data = self.repository.get_customer_segments(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list[dict]) -> CustomerSegmentsResponse:
        """Map database rows to CustomerSegmentsResponse."""
        segments = [
            CustomerSegmentItem(
                segment_name=str(row.get("SEGMENT_NAME") or ""),
                customer_count=int(row.get("CUSTOMER_COUNT") or 0)
            )
            for row in data
        ]
        return CustomerSegmentsResponse(segments=segments)


# Singleton instance for dependency injection
customer_segments_service = CustomerSegmentsService()
