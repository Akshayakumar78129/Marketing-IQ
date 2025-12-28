"""
Meta Ads Engagement - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class MetaAdsEngagementResponse(BaseModel):
    """Response model for Meta Ads engagement metrics."""
    link_clicks: int = Field(..., description="Total link clicks")
    post_engagements: int = Field(..., description="Total post engagements")
    page_engagements: int = Field(..., description="Total page engagements")
    post_reactions: int = Field(..., description="Total post reactions")
    view_content: int = Field(..., description="Total view content actions")
    add_to_cart: int = Field(..., description="Total add to cart actions")
    initiate_checkout: int = Field(..., description="Total initiate checkout actions")
    purchases: int = Field(..., description="Total purchases")
    total_actions: int = Field(..., description="Total actions")
    view_to_cart_rate: float = Field(..., description="View to cart conversion rate")
    cart_to_checkout_rate: float = Field(..., description="Cart to checkout conversion rate")
    checkout_to_purchase_rate: float = Field(..., description="Checkout to purchase conversion rate")

    class Config:
        from_attributes = True
