"""
Google Ads Ad Group Performance - Pydantic models (DTOs).
"""
from typing import Optional
from pydantic import BaseModel, Field


class AdGroupPerformanceItem(BaseModel):
    """Response model for a single ad group's performance metrics."""
    ad_group: str = Field(..., description="Ad group name")
    campaign: str = Field(..., description="Campaign name")
    impressions: int = Field(..., description="Total impressions")
    clicks: int = Field(..., description="Total clicks")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")
    conversions: int = Field(..., description="Total conversions")
    cvr: float = Field(..., description="Conversion Rate percentage")

    class Config:
        from_attributes = True


class AdGroupPerformanceResponse(BaseModel):
    """Response model for list of ad group performance metrics."""
    items: list[AdGroupPerformanceItem] = Field(..., description="List of ad group performance records")
    total: int = Field(..., description="Total number of ad groups")

    class Config:
        from_attributes = True
