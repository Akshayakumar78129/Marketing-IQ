"""
Monthly Conversions - Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class MonthlyConversion(BaseModel):
    """Model for a single month's conversion metrics."""
    month: str = Field(..., description="Month label (e.g., 'Nov 2025')")
    conversions: float = Field(..., description="Total number of conversions for the month")

    class Config:
        from_attributes = True


class MonthlyConversionsResponse(BaseModel):
    """Response model for monthly conversions trend."""
    items: List[MonthlyConversion] = Field(..., description="List of monthly conversion data points")
    total_conversions: float = Field(..., description="Total conversions across all months")

    class Config:
        from_attributes = True
