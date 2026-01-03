"""
Conversions by Channel service - Business logic layer for channel conversion metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import conversions_by_channel_repository
from .models import ConversionsByChannelResponse, ChannelConversion


class ConversionsByChannelService:
    """Service class for conversions by channel business logic."""

    def __init__(self, repository=conversions_by_channel_repository):
        self.repository = repository

    def get_conversions_by_channel(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> ConversionsByChannelResponse:
        """
        Get conversions grouped by marketing channel.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            ConversionsByChannelResponse with channel conversion metrics

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
        data = self.repository.get_conversions_by_channel(date_from, date_to)

        # Map database results to response model
        return self._map_to_response(data)

    @staticmethod
    def _map_to_response(data: list) -> ConversionsByChannelResponse:
        """Map database rows to ConversionsByChannelResponse."""
        items = [
            ChannelConversion(
                channel=row.get("CHANNEL") or "Unknown",
                conversions=int(row.get("CONVERSIONS") or 0),
                revenue=float(row.get("REVENUE") or 0)
            )
            for row in data
        ]

        total_conversions = sum(item.conversions for item in items)
        total_revenue = sum(item.revenue for item in items)

        return ConversionsByChannelResponse(
            items=items,
            total_conversions=total_conversions,
            total_revenue=round(total_revenue, 2)
        )


# Singleton instance for dependency injection
conversions_by_channel_service = ConversionsByChannelService()
