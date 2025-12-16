"""
Google Ads Overview - Pydantic models (DTOs).
"""
from typing import Optional
from pydantic import BaseModel, Field


class GoogleAdsOverviewResponse(BaseModel):
    """Response model for Google Ads overview metrics."""
    total_spend: float = Field(..., description="Total advertising spend")
    total_conversions: float = Field(..., description="Total number of conversions")
    total_revenue: float = Field(..., description="Total conversion value/revenue")
    roas: float = Field(..., description="Return on Ad Spend (Revenue/Spend)")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")
    avg_quality_score: Optional[float] = Field(None, description="Average Quality Score across keywords")

    class Config:
        from_attributes = True
