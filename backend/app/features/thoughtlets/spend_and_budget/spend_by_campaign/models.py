"""
Thoughtlets Spend and Budget - Spend by Campaign - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class CampaignSpend(BaseModel):
    """Model for spend data of a single campaign."""
    campaign: str = Field(..., description="Campaign name")
    platform: str = Field(..., description="Platform name (e.g., Google Ads, Meta Ads)")
    status: str = Field(..., description="Campaign status (e.g., ENABLED, ACTIVE)")
    spend: float = Field(..., description="Total spend for this campaign")
    revenue: float = Field(..., description="Total revenue (conversion value)")
    roas: float = Field(..., description="Return on Ad Spend")
    conversions: float = Field(..., description="Total conversions")
    cpc: float = Field(..., description="Cost per click")


class SpendByCampaignResponse(BaseModel):
    """Response model for spend by campaign."""
    items: list[CampaignSpend] = Field(..., description="List of campaign spend data")

    class Config:
        from_attributes = True
