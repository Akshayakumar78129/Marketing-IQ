"""
Creative & Messaging - Ad Set Performance Pydantic models (DTOs).
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class AdSetPerformanceItem(BaseModel):
    """Single ad set performance item for table."""
    ad_set: str = Field(..., description="Name of the ad set")
    campaign: str = Field(..., description="Name of the campaign")
    impressions: int = Field(..., description="Total impressions")
    reach: int = Field(..., description="Total reach")
    clicks: int = Field(..., description="Total clicks")
    ctr: float = Field(..., description="Average Click-Through Rate")
    cpc: Optional[float] = Field(None, description="Average Cost Per Click")
    spend: float = Field(..., description="Total spend")


class AdSetPerformanceResponse(BaseModel):
    """Response model for Ad Set Performance table data."""
    data: List[AdSetPerformanceItem] = Field(..., description="List of ad set performance records")

    class Config:
        from_attributes = True
