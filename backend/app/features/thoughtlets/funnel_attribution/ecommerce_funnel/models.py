"""
eCommerce Funnel - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class EcommerceFunnelResponse(BaseModel):
    """Response model for eCommerce funnel metrics (View → Cart → Purchase journey)."""
    views: int = Field(..., description="Total number of product views")
    add_to_cart: int = Field(..., description="Total number of items added to cart")
    purchase: int = Field(..., description="Total number of items purchased")

    class Config:
        from_attributes = True
