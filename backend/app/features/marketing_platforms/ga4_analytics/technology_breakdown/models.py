"""
GA4 Analytics Technology Breakdown - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class TrafficSourceItem(BaseModel):
    """Response model for a single traffic source."""
    source: str = Field(..., description="Traffic source name")
    sessions: int = Field(..., description="Number of sessions from this source")
    percentage: float = Field(..., description="Percentage of total sessions")

    class Config:
        from_attributes = True


class DeviceItem(BaseModel):
    """Response model for a single device category."""
    device_category: str = Field(..., description="Device category (desktop, mobile, tablet, etc.)")
    users: int = Field(..., description="Number of users on this device")
    percentage: float = Field(..., description="Percentage of total users")

    class Config:
        from_attributes = True


class BrowserItem(BaseModel):
    """Response model for a single browser."""
    browser: str = Field(..., description="Browser name")
    users: int = Field(..., description="Number of users on this browser")
    percentage: float = Field(..., description="Percentage of total users")

    class Config:
        from_attributes = True


class TechnologyBreakdownResponse(BaseModel):
    """Response model for technology breakdown metrics."""
    traffic_sources: list[TrafficSourceItem] = Field(..., description="Traffic sources breakdown")
    devices: list[DeviceItem] = Field(..., description="Devices breakdown")
    browsers: list[BrowserItem] = Field(..., description="Browsers breakdown")

    class Config:
        from_attributes = True
