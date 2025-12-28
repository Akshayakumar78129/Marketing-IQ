"""
Meta Ads Device service - Business logic layer for device metrics.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import meta_ads_device_repository
from .models import MetaAdsDeviceResponse, MetaAdsDeviceListResponse


class MetaAdsDeviceService:
    """Service class for Meta Ads device business logic."""

    def __init__(self, repository=meta_ads_device_repository):
        self.repository = repository

    def get_devices(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        device: Optional[str] = None
    ) -> MetaAdsDeviceListResponse:
        """
        Get Meta Ads device metrics.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics
            device: Optional device filter

        Returns:
            MetaAdsDeviceListResponse with list of device metrics

        Raises:
            HTTPException: 400 if date_from > date_to
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch devices from repository
        devices_data = self.repository.get_devices(date_from, date_to, device)

        # Map database results to response models
        devices = [self._map_to_response(row) for row in devices_data]

        return MetaAdsDeviceListResponse(
            devices=devices,
            total_count=len(devices)
        )

    @staticmethod
    def _map_to_response(data: dict) -> MetaAdsDeviceResponse:
        """Map database row (uppercase keys) to response model."""
        return MetaAdsDeviceResponse(
            device=str(data.get("DEVICE") or ""),
            impressions=int(data.get("TOTAL_IMPRESSIONS") or 0),
            reach=int(data.get("TOTAL_REACH") or 0),
            spend=float(data.get("TOTAL_SPEND") or 0),
            clicks=int(data.get("TOTAL_CLICKS") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0)
        )


# Singleton instance for dependency injection
meta_ads_device_service = MetaAdsDeviceService()
