"""
Thoughtlets Core Performance ROAS by Platform - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class RoasByPlatformItem(BaseModel):
    """Response model for a single platform's ROAS."""
    platform: str = Field(..., description="Platform name (e.g., 'Google Ads', 'Meta Ads')")
    roas: float = Field(..., description="Return on ad spend (revenue/spend)")

    class Config:
        from_attributes = True


class RoasByPlatformResponse(BaseModel):
    """Response model for ROAS by platform data."""
    platforms: list[RoasByPlatformItem] = Field(..., description="List of platforms with ROAS")

    class Config:
        from_attributes = True
