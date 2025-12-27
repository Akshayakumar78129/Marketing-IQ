"""
GA4 Analytics Daily Traffic Trend - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class DailyTrafficItem(BaseModel):
    """Response model for a single day's traffic data."""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    sessions: int = Field(..., description="Total number of sessions")
    users: int = Field(..., description="Total number of users")

    class Config:
        from_attributes = True


class DailyTrafficTrendResponse(BaseModel):
    """Response model for daily traffic trend list."""
    items: list[DailyTrafficItem] = Field(..., description="List of daily traffic data points")
    total: int = Field(..., description="Total number of data points")

    class Config:
        from_attributes = True
