"""
Meta Ads Funnel - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class MetaAdsFunnelResponse(BaseModel):
    """Response model for Meta Ads funnel metrics (Meta pixel conversion events)."""
    view_content: int = Field(..., description="Total View Content events")
    add_to_cart: int = Field(..., description="Total Add to Cart events")
    initiate_checkout: int = Field(..., description="Total Initiate Checkout events")
    purchase: int = Field(..., description="Total Purchase events")

    class Config:
        from_attributes = True
