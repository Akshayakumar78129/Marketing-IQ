"""
Thoughtlets Core Performance Conversions Trend - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class ConversionsTrendItem(BaseModel):
    """Response model for a single month's conversions."""
    month: str = Field(..., description="Month in 'Mon YYYY' format (e.g., 'Jan 2025')")
    conversions: float = Field(..., description="Total conversions for the month")

    class Config:
        from_attributes = True


class ConversionsTrendResponse(BaseModel):
    """Response model for conversions trend data."""
    trend: list[ConversionsTrendItem] = Field(..., description="List of monthly conversion data")

    class Config:
        from_attributes = True
