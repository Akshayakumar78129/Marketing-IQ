"""
Google Ads Campaign Performance - Pydantic models (DTOs).
"""
from typing import Optional
from pydantic import BaseModel, Field


class CampaignPerformanceItem(BaseModel):
    """Response model for a single campaign's performance metrics."""
    campaign: str = Field(..., description="Campaign name")
    status: str = Field(..., description="Campaign status (Active, Paused, etc.)")
    spend: float = Field(..., description="Total advertising spend")
    revenue: float = Field(..., description="Total conversion value/revenue")
    roas: float = Field(..., description="Return on Ad Spend (Revenue/Spend)")
    conversions: int = Field(..., description="Total number of conversions")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")

    class Config:
        from_attributes = True


class CampaignPerformanceListResponse(BaseModel):
    """Response model for list of campaign performance metrics."""
    items: list[CampaignPerformanceItem] = Field(..., description="List of campaign performance records")
    total: int = Field(..., description="Total number of campaigns")

    class Config:
        from_attributes = True
