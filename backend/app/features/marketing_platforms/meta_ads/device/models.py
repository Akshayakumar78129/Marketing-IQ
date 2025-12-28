"""
Meta Ads Device - Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class MetaAdsDeviceResponse(BaseModel):
    """Response model for a single device's metrics."""
    device: str = Field(..., description="Device type (mobile_app, desktop, mobile_web)")
    impressions: int = Field(..., description="Total number of impressions")
    reach: int = Field(..., description="Total unique users reached")
    spend: float = Field(..., description="Total advertising spend")
    clicks: int = Field(..., description="Total number of clicks")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")

    class Config:
        from_attributes = True


class MetaAdsDeviceListResponse(BaseModel):
    """Response model for list of device metrics."""
    devices: List[MetaAdsDeviceResponse] = Field(..., description="List of device metrics")
    total_count: int = Field(..., description="Total number of devices")

    class Config:
        from_attributes = True
