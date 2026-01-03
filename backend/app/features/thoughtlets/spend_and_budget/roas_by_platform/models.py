"""
Thoughtlets Spend and Budget - ROAS by Platform - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class PlatformROAS(BaseModel):
    """Model for ROAS data of a single platform."""
    platform: str = Field(..., description="Platform name (e.g., Google Ads, Meta Ads)")
    roas: float = Field(..., description="Return on Ad Spend for this platform")


class ROASByPlatformResponse(BaseModel):
    """Response model for ROAS by platform breakdown."""
    items: list[PlatformROAS] = Field(..., description="List of platform ROAS data")

    class Config:
        from_attributes = True
