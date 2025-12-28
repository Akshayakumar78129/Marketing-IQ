"""
GA4 Analytics Landing Pages - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class LandingPageItem(BaseModel):
    """Response model for a single landing page."""
    page: str = Field(..., description="Page path")
    entrances: int = Field(..., description="Number of entrances (entry points)")
    bounce_rate: float = Field(..., description="Bounce rate percentage")
    sessions: int = Field(..., description="Number of sessions")

    class Config:
        from_attributes = True


class LandingPagesResponse(BaseModel):
    """Response model for landing pages list."""
    pages: list[LandingPageItem] = Field(..., description="List of landing pages")

    class Config:
        from_attributes = True
