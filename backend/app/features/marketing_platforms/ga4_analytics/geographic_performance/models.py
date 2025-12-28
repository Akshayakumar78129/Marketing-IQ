"""
GA4 Analytics Geographic Performance - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class GeographicPerformanceItem(BaseModel):
    """Response model for a single country's performance."""
    country: str = Field(..., description="Country name")
    sessions: int = Field(..., description="Number of sessions")
    conv_rate: float = Field(..., description="Conversion rate percentage")
    revenue: float = Field(..., description="Total revenue")

    class Config:
        from_attributes = True


class GeographicPerformanceResponse(BaseModel):
    """Response model for geographic performance list."""
    countries: list[GeographicPerformanceItem] = Field(..., description="List of countries with performance metrics")

    class Config:
        from_attributes = True
