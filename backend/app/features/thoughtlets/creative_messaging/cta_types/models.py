"""
Creative & Messaging - CTA Types Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class CTATypeItem(BaseModel):
    """Single CTA type item for bar chart."""
    cta_type: str = Field(..., description="Call to action type (e.g., SHOP_NOW, LEARN_MORE)")
    count: int = Field(..., description="Number of creatives with this CTA type")


class CTATypesResponse(BaseModel):
    """Response model for CTA Types bar chart data."""
    data: List[CTATypeItem] = Field(..., description="List of CTA types with counts")

    class Config:
        from_attributes = True
