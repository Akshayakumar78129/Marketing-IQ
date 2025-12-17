"""
Meta Ads Placements - Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class MetaAdsPlacementResponse(BaseModel):
    """Response model for a single placement's metrics."""
    placement: str = Field(..., description="Placement name (facebook, instagram, etc.)")
    impressions: int = Field(..., description="Total number of impressions")
    reach: int = Field(..., description="Total unique users reached")
    spend: float = Field(..., description="Total advertising spend")
    clicks: int = Field(..., description="Total number of clicks")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")

    class Config:
        from_attributes = True


class MetaAdsPlacementsListResponse(BaseModel):
    """Response model for list of placements."""
    placements: List[MetaAdsPlacementResponse] = Field(..., description="List of placements")
    total_count: int = Field(..., description="Total number of placements")

    class Config:
        from_attributes = True
