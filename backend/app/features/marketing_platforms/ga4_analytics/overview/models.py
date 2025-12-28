"""
GA4 Analytics Overview - Pydantic models (DTOs).
"""
from typing import Optional
from pydantic import BaseModel, Field


class GA4OverviewResponse(BaseModel):
    """Response model for GA4 Analytics overview metrics."""
    sessions: int = Field(..., description="Total number of sessions")
    users: int = Field(..., description="Total number of users")
    engaged_sessions: int = Field(..., description="Number of engaged sessions")
    engagement_rate: float = Field(..., description="Engagement rate percentage")
    sessions_per_user: float = Field(..., description="Average sessions per user")
    conversions: float = Field(..., description="Total number of conversions")
    revenue: float = Field(..., description="Total revenue")
    conversion_value: Optional[float] = Field(None, description="Average conversion value")

    class Config:
        from_attributes = True
