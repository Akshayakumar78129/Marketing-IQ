"""
Traffic by Source - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class TrafficSourceItem(BaseModel):
    """Single traffic source with session count."""
    source_medium: str = Field(..., description="Source/medium combination (e.g., 'google / organic')")
    sessions: int = Field(..., description="Number of sessions from this source")

    class Config:
        from_attributes = True


class TrafficBySourceResponse(BaseModel):
    """Response model for traffic by source distribution."""
    items: list[TrafficSourceItem] = Field(..., description="List of traffic sources with session counts")
    total_sessions: int = Field(..., description="Total sessions across all sources")

    class Config:
        from_attributes = True
