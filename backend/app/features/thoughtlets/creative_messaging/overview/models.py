"""
Creative & Messaging - Overview Pydantic models (DTOs).
"""
from typing import Optional
from pydantic import BaseModel, Field


class OverviewResponse(BaseModel):
    """Response model for Creative & Messaging overview KPI metrics."""
    total_creatives: int = Field(..., description="Total number of creatives with performance data")
    image_creatives: int = Field(..., description="Number of image creatives")
    video_creatives: int = Field(..., description="Number of video creatives")
    avg_ctr: float = Field(..., description="Average Click-Through Rate")
    avg_cvr: Optional[float] = Field(None, description="Average Conversion Rate (conversions/clicks)")
    avg_cpc: float = Field(..., description="Average Cost Per Click")
    cpm: float = Field(..., description="Cost Per Mille (thousand impressions)")
    overall_roas: Optional[float] = Field(None, description="Overall Return on Ad Spend")

    class Config:
        from_attributes = True
