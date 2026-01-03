"""
Traffic Source Attribution - Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class TrafficSourceAttribution(BaseModel):
    """Model for a single traffic source attribution row."""
    source_medium: str = Field(..., description="Source / Medium combination (e.g., '(direct) / (none)')")
    sessions: int = Field(..., description="Total number of sessions from this source")
    engaged: int = Field(..., description="Number of engaged sessions")
    users: int = Field(..., description="Number of unique users")
    engagement_rate_pct: float = Field(..., description="Engagement rate percentage")
    sessions_per_user: float = Field(..., description="Average sessions per user")

    class Config:
        from_attributes = True


class TrafficSourceAttributionResponse(BaseModel):
    """Response model for traffic source attribution data."""
    items: List[TrafficSourceAttribution] = Field(..., description="List of traffic source attribution rows")
    total_sessions: int = Field(..., description="Total sessions across all sources")
    total_users: int = Field(..., description="Total unique users across all sources")

    class Config:
        from_attributes = True
