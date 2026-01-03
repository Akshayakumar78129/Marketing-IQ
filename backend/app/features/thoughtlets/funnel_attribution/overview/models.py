"""
Funnel & Attribution Overview - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class FunnelAttributionOverviewResponse(BaseModel):
    """Response model for funnel and attribution metrics."""
    total_sessions: int = Field(..., description="Total number of sessions")
    engagement_rate: float = Field(..., description="Engagement rate percentage")
    view_to_cart_pct: float = Field(..., description="View-to-Cart percentage")
    cart_to_purchase_pct: float = Field(..., description="Cart-to-Purchase percentage")
    cart_abandon_rate: float = Field(..., description="Cart abandonment rate percentage")
    total_conversions: int = Field(..., description="Total number of conversions")
    utm_coverage_pct: float = Field(..., description="UTM coverage percentage")
    avg_order_value: float = Field(..., description="Average order value")

    class Config:
        from_attributes = True
