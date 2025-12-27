"""
GA4 Analytics Hourly Traffic Pattern - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class HourlyTrafficItem(BaseModel):
    """Response model for a single hour's traffic data."""
    hour: int = Field(..., description="Hour of day (0-23)")
    hour_label: str = Field(..., description="Human-readable hour label (e.g., '12 AM', '1 PM')")
    impressions: int = Field(..., description="Total number of impressions")
    clicks: int = Field(..., description="Total number of clicks")

    class Config:
        from_attributes = True


class HourlyTrafficPatternResponse(BaseModel):
    """Response model for hourly traffic pattern list."""
    items: list[HourlyTrafficItem] = Field(..., description="List of hourly traffic data points")
    total: int = Field(..., description="Total number of data points")

    class Config:
        from_attributes = True
