"""
Thoughtlets Spend and Budget - Spend by Ad Group - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class AdGroupSpend(BaseModel):
    """Model for spend data of a single ad group."""
    campaign: str = Field(..., description="Ad group name")
    impressions: int = Field(..., description="Total impressions")
    clicks: int = Field(..., description="Total clicks")
    spend: float = Field(..., description="Total spend")
    conversions: float = Field(..., description="Total conversions")
    roas: float = Field(..., description="Return on Ad Spend")


class SpendByAdGroupResponse(BaseModel):
    """Response model for spend by ad group."""
    items: list[AdGroupSpend] = Field(..., description="List of ad group spend data")

    class Config:
        from_attributes = True
