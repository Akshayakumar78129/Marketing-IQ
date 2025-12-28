"""
GA4 Analytics Technology Breakdown service - Business logic layer for technology operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import ga4_technology_breakdown_repository
from .models import (
    TrafficSourceItem,
    DeviceItem,
    BrowserItem,
    TechnologyBreakdownResponse
)


class GA4TechnologyBreakdownService:
    """Service class for GA4 Analytics technology breakdown business logic."""

    def __init__(self, repository=ga4_technology_breakdown_repository):
        self.repository = repository

    def get_technology_breakdown(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> TechnologyBreakdownResponse:
        """
        Get technology breakdown metrics, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            TechnologyBreakdownResponse with traffic sources, devices, and browsers

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch all breakdowns from repository
        traffic_sources = self.repository.get_traffic_sources(date_from, date_to)
        devices = self.repository.get_devices(date_from, date_to)
        browsers = self.repository.get_browsers(date_from, date_to)

        # Map database results to response models
        return TechnologyBreakdownResponse(
            traffic_sources=[self._map_to_traffic_source(row) for row in traffic_sources],
            devices=[self._map_to_device(row) for row in devices],
            browsers=[self._map_to_browser(row) for row in browsers]
        )

    @staticmethod
    def _map_to_traffic_source(data: dict) -> TrafficSourceItem:
        """Map database row to TrafficSourceItem."""
        return TrafficSourceItem(
            source=str(data.get("SOURCE") or "unknown"),
            sessions=int(data.get("SESSIONS") or 0),
            percentage=float(data.get("PERCENTAGE") or 0)
        )

    @staticmethod
    def _map_to_device(data: dict) -> DeviceItem:
        """Map database row to DeviceItem."""
        return DeviceItem(
            device_category=str(data.get("DEVICE_CATEGORY") or "unknown"),
            users=int(data.get("USERS") or 0),
            percentage=float(data.get("PERCENTAGE") or 0)
        )

    @staticmethod
    def _map_to_browser(data: dict) -> BrowserItem:
        """Map database row to BrowserItem."""
        return BrowserItem(
            browser=str(data.get("BROWSER") or "unknown"),
            users=int(data.get("USERS") or 0),
            percentage=float(data.get("PERCENTAGE") or 0)
        )


# Singleton instance for dependency injection
ga4_technology_breakdown_service = GA4TechnologyBreakdownService()
