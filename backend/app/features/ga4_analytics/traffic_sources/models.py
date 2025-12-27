"""
GA4 Analytics Traffic Sources - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class TrafficSourceItem(BaseModel):
    """Response model for a single traffic source."""
    source: str = Field(..., description="Traffic source name")
    sessions: int = Field(..., description="Total number of sessions")
    users: int = Field(..., description="Total number of users")
    revenue: float = Field(..., description="Total revenue")

    class Config:
        from_attributes = True


class TrafficSourcesListResponse(BaseModel):
    """Response model for traffic sources list."""
    items: list[TrafficSourceItem] = Field(..., description="List of traffic sources")
    total: int = Field(..., description="Total number of traffic sources")

    class Config:
        from_attributes = True
