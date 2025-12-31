"""
Search & Keywords - Search Campaigns Performance Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class SearchCampaignItem(BaseModel):
    """Individual search campaign performance item."""
    campaign: str = Field(..., description="Campaign name")
    type: str = Field(..., description="Campaign type (SEARCH, PERFORMANCE_MAX)")
    status: str = Field(..., description="Campaign status")
    impressions: int = Field(..., description="Total impressions")
    clicks: int = Field(..., description="Total clicks")
    ctr: float = Field(..., description="Click-through rate percentage")
    spend: float = Field(..., description="Total spend")
    conversions: float = Field(..., description="Total conversions")
    roas: float = Field(..., description="Return on ad spend")

    class Config:
        from_attributes = True


class SearchCampaignsResponse(BaseModel):
    """Response model for search campaigns list."""
    campaigns: List[SearchCampaignItem] = Field(..., description="List of search campaign performance data")
