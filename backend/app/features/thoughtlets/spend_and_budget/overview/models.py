"""
Thoughtlets Spend and Budget Overview - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class SpendAndBudgetOverviewResponse(BaseModel):
    """Response model for spend and budget metrics across all platforms."""
    total_spend: float = Field(..., description="Total spend across all platforms")
    total_revenue: float = Field(..., description="Total revenue (conversion value)")
    overall_roas: float = Field(..., description="Overall return on ad spend (revenue/spend)")
    cost_per_conversion: float = Field(..., description="Cost per conversion (spend/conversions)")
    avg_cpc: float = Field(..., description="Average cost per click (spend/clicks)")
    avg_daily_spend: float = Field(..., description="Average daily spend")
    total_impressions: int = Field(..., description="Total number of impressions")
    conversions: int = Field(..., description="Total number of conversions")

    class Config:
        from_attributes = True
