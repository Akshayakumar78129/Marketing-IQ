"""
Creative & Messaging - Creative Type Distribution Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class CreativeTypeItem(BaseModel):
    """Single creative type item for pie chart."""
    creative_type: str = Field(..., description="Type of creative (image or video)")
    count: int = Field(..., description="Number of creatives of this type")


class CreativeTypeDistributionResponse(BaseModel):
    """Response model for Creative Type Distribution pie chart data."""
    data: List[CreativeTypeItem] = Field(..., description="List of creative types with counts")

    class Config:
        from_attributes = True
