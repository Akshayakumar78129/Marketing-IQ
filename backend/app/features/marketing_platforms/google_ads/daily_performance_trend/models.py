"""
Google Ads Daily Performance Trend - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class DailyPerformanceTrendItem(BaseModel):
    """Response model for daily performance trend by day of week."""
    day_name: str = Field(..., description="Day of week name (e.g., Monday, Tuesday)")
    day_order: int = Field(..., description="Day order for sorting (1=Monday, 7=Sunday)")
    total_conversions: float = Field(..., description="Total conversions for this day")
    total_spend: float = Field(..., description="Total spend for this day")

    class Config:
        from_attributes = True


class DailyPerformanceTrendResponse(BaseModel):
    """Response model for daily performance trend."""
    items: list[DailyPerformanceTrendItem] = Field(..., description="List of daily performance data")
    total: int = Field(..., description="Total number of days")

    class Config:
        from_attributes = True
