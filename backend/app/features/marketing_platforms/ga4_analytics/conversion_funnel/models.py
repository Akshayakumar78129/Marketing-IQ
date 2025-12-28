"""
GA4 Analytics Conversion Funnel - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class ConversionFunnelResponse(BaseModel):
    """Response model for conversion funnel metrics."""
    sessions: int = Field(..., description="Total number of sessions")
    product_views: int = Field(..., description="Total number of product views")
    add_to_cart: int = Field(..., description="Total number of add to cart events")
    purchases: int = Field(..., description="Total number of purchases")

    class Config:
        from_attributes = True
