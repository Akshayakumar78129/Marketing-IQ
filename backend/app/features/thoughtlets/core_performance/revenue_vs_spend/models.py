"""
Thoughtlets Core Performance Revenue vs Spend - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class RevenueVsSpendItem(BaseModel):
    """Response model for a single month's revenue and spend."""
    month: str = Field(..., description="Month in 'Mon YYYY' format (e.g., 'Jan 2025')")
    revenue: float = Field(..., description="Total revenue (conversion value) for the month")
    spend: float = Field(..., description="Total ad spend for the month")

    class Config:
        from_attributes = True


class RevenueVsSpendResponse(BaseModel):
    """Response model for revenue vs spend data."""
    data: list[RevenueVsSpendItem] = Field(..., description="List of monthly revenue and spend data")

    class Config:
        from_attributes = True
