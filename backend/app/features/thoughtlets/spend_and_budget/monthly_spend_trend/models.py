"""
Thoughtlets Spend and Budget - Monthly Spend Trend - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class MonthlySpend(BaseModel):
    """Model for spend data of a single month."""
    month: str = Field(..., description="Month in YYYY-MM format")
    spend: float = Field(..., description="Total spend for this month")


class MonthlySpendTrendResponse(BaseModel):
    """Response model for monthly spend trend data."""
    items: list[MonthlySpend] = Field(..., description="List of monthly spend data points")

    class Config:
        from_attributes = True
