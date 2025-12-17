"""
Google Ads Spend by Campaign Type - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class SpendByCampaignTypeItem(BaseModel):
    """Response model for spend by a single campaign type."""
    campaign_type: str = Field(..., description="Campaign type (e.g., Search, Shopping, Performance Max)")
    total_spend: float = Field(..., description="Total advertising spend for this campaign type")
    spend_percentage: float = Field(..., description="Percentage of total spend")

    class Config:
        from_attributes = True


class SpendByCampaignTypeResponse(BaseModel):
    """Response model for spend by campaign type breakdown."""
    items: list[SpendByCampaignTypeItem] = Field(..., description="List of spend by campaign type")
    total: int = Field(..., description="Total number of campaign types")

    class Config:
        from_attributes = True
