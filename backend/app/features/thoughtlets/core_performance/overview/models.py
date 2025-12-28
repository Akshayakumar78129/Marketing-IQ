"""
Thoughtlets Core Performance Overview - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class CorePerformanceOverviewResponse(BaseModel):
    """Response model for core performance metrics across all platforms."""
    conversions: float = Field(..., description="Total number of conversions")
    conversion_rate: float = Field(..., description="Conversion rate percentage (conversions/clicks * 100)")
    cost_per_conversion: float = Field(..., description="Cost per conversion (spend/conversions)")
    revenue: float = Field(..., description="Total revenue (conversion value)")
    roas: float = Field(..., description="Return on ad spend (revenue/spend)")
    ctr: float = Field(..., description="Click-through rate percentage (clicks/impressions * 100)")
    cpc: float = Field(..., description="Cost per click (spend/clicks)")
    impressions: int = Field(..., description="Total number of impressions")

    class Config:
        from_attributes = True
