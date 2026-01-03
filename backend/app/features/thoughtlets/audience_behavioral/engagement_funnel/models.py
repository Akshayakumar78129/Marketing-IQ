"""
Engagement Funnel - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class EngagementFunnelResponse(BaseModel):
    """Response model for engagement funnel metrics."""
    total_users: int = Field(..., description="Total unique users")
    sessions: int = Field(..., description="Total number of sessions")
    engaged: int = Field(..., description="Number of engaged sessions")
    conversions: int = Field(..., description="Total number of conversions")

    class Config:
        from_attributes = True
