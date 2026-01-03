"""
Top Pages - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class PageItem(BaseModel):
    """Single page with engagement metrics."""
    page_path: str = Field(..., description="Page path (e.g., '/', '/store', '/checkout/')")
    page_type: str = Field(..., description="Page type (Homepage, Other, Collection Page, Checkout, Product Page)")
    views: int = Field(..., description="Total page views")
    users: int = Field(..., description="Number of users who viewed this page")
    avg_time_seconds: float = Field(..., description="Average time on page in seconds")
    views_per_user: float = Field(..., description="Average views per user")

    class Config:
        from_attributes = True


class TopPagesResponse(BaseModel):
    """Response model for top pages with engagement metrics."""
    items: list[PageItem] = Field(..., description="List of pages with engagement metrics")
    total_pages: int = Field(..., description="Total number of unique pages")

    class Config:
        from_attributes = True
