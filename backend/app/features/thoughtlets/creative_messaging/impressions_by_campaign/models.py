"""
Creative & Messaging - Impressions by Campaign Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class CampaignImpressionsItem(BaseModel):
    """Single campaign impressions item for bar chart."""
    campaign_name: str = Field(..., description="Name of the campaign")
    impressions: int = Field(..., description="Total impressions for this campaign")


class ImpressionsByCampaignResponse(BaseModel):
    """Response model for Impressions by Campaign bar chart data."""
    data: List[CampaignImpressionsItem] = Field(..., description="List of campaigns with impressions")

    class Config:
        from_attributes = True
