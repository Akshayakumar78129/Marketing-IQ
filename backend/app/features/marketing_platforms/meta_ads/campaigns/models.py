"""
Meta Ads Campaigns - Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class MetaAdsCampaignResponse(BaseModel):
    """Response model for a single Meta Ads campaign."""
    campaign_id: str = Field(..., description="Campaign ID")
    campaign_name: str = Field(..., description="Campaign name")
    status: str = Field(..., description="Campaign status")
    total_spend: float = Field(..., description="Total advertising spend")
    impressions: int = Field(..., description="Total number of impressions")
    clicks: int = Field(..., description="Total number of clicks")
    conversions: float = Field(..., description="Total number of conversions")
    revenue: float = Field(..., description="Total revenue from conversions")
    roas: float = Field(..., description="Return on Ad Spend")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")
    cpm: float = Field(..., description="Cost Per Mille (1000 impressions)")

    class Config:
        from_attributes = True


class MetaAdsCampaignsListResponse(BaseModel):
    """Response model for list of Meta Ads campaigns."""
    campaigns: List[MetaAdsCampaignResponse] = Field(..., description="List of campaigns")
    total_count: int = Field(..., description="Total number of campaigns")

    class Config:
        from_attributes = True
