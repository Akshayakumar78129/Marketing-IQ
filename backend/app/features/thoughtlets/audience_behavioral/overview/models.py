"""
Audience & Behavioral Overview - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class AudienceBehavioralOverviewResponse(BaseModel):
    """Response model for Audience & Behavioral overview metrics."""
    total_users: int = Field(..., description="Total number of users")
    total_sessions: int = Field(..., description="Total number of sessions")
    new_users: int = Field(..., description="Number of new users")
    returning_users: int = Field(..., description="Number of returning users")
    engagement_rate: float = Field(..., description="Engagement rate percentage")
    bounce_rate: float = Field(..., description="Bounce rate percentage")
    sessions_per_user: float = Field(..., description="Average sessions per user")
    conversion_rate: float = Field(..., description="Conversion rate percentage")

    class Config:
        from_attributes = True
