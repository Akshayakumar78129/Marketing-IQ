"""
Thoughtlets Spend and Budget - Spend by Platform - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class PlatformSpend(BaseModel):
    """Model for spend data of a single platform."""
    platform: str = Field(..., description="Platform name (e.g., Google Ads, Meta Ads)")
    spend: float = Field(..., description="Total spend for this platform")


class SpendByPlatformResponse(BaseModel):
    """Response model for spend by platform breakdown."""
    items: list[PlatformSpend] = Field(..., description="List of platform spend data")
    total_spend: float = Field(..., description="Total spend across all platforms")

    class Config:
        from_attributes = True
