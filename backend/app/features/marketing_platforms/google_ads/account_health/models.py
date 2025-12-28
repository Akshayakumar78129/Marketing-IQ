"""
Google Ads Account Health - Pydantic models (DTOs).
"""
from typing import Optional
from pydantic import BaseModel, Field


class AccountHealthResponse(BaseModel):
    """Response model for account health metrics."""
    total_campaigns: int = Field(..., description="Total number of campaigns")
    active_campaigns: int = Field(..., description="Number of active (enabled) campaigns")
    avg_roas: Optional[float] = Field(None, description="Average Return on Ad Spend")
    total_keywords: int = Field(..., description="Total number of keywords")

    class Config:
        from_attributes = True
