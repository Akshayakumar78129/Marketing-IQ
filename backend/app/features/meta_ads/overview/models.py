"""
Meta Ads Overview - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class MetaAdsOverviewResponse(BaseModel):
    """Response model for Meta Ads overview metrics."""
    total_spend: float = Field(..., description="Total advertising spend")
    impressions: int = Field(..., description="Total number of impressions")
    reach: int = Field(..., description="Total unique users reached")
    clicks: int = Field(..., description="Total number of clicks")
    conversions: float = Field(..., description="Total number of conversions")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")
    cpm: float = Field(..., description="Cost Per Mille (1000 impressions)")
    roas: float = Field(..., description="Return on Ad Spend")

    class Config:
        from_attributes = True
