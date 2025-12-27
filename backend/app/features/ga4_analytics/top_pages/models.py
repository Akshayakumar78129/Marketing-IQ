"""
GA4 Analytics Top Pages - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class TopPageItem(BaseModel):
    """Response model for a single page."""
    page: str = Field(..., description="Page path")
    page_views: int = Field(..., description="Number of page views")
    unique_views: int = Field(..., description="Number of unique views (users)")
    avg_time_seconds: float = Field(..., description="Average time on page in seconds")
    bounce_rate: float = Field(..., description="Bounce rate percentage (not available at page level, returns 0)")

    class Config:
        from_attributes = True


class TopPagesResponse(BaseModel):
    """Response model for top pages list."""
    pages: list[TopPageItem] = Field(..., description="List of top pages")

    class Config:
        from_attributes = True
