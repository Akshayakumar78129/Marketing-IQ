"""
Creative & Messaging - CTR by Campaign Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class CampaignCTRItem(BaseModel):
    """Single campaign CTR item for bar chart."""
    campaign_name: str = Field(..., description="Name of the campaign")
    ctr: float = Field(..., description="Average Click-Through Rate for this campaign")


class CTRByCampaignResponse(BaseModel):
    """Response model for CTR by Campaign bar chart data."""
    data: List[CampaignCTRItem] = Field(..., description="List of campaigns with CTR")

    class Config:
        from_attributes = True
