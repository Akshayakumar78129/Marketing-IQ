"""
Meta Ads Ad Sets - Pydantic models (DTOs).
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class MetaAdsAdSetResponse(BaseModel):
    """Response model for a single ad set's metrics."""
    ad_set_id: str = Field(..., description="Ad set identifier")
    ad_set_name: str = Field(..., description="Ad set name")
    campaign_name: str = Field(..., description="Campaign name")
    spend: float = Field(..., description="Total advertising spend")
    reach: int = Field(..., description="Total unique users reached")
    clicks: int = Field(..., description="Total number of clicks")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")
    impressions: int = Field(..., description="Total number of impressions")

    class Config:
        from_attributes = True


class MetaAdsAdSetListResponse(BaseModel):
    """Response model for list of ad set metrics."""
    ad_sets: List[MetaAdsAdSetResponse] = Field(..., description="List of ad set metrics")
    total_count: int = Field(..., description="Total number of ad sets")

    class Config:
        from_attributes = True
