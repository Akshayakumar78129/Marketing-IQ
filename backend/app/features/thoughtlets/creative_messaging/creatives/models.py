"""
Creative & Messaging - Creatives Pydantic models (DTOs).
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class CreativeItem(BaseModel):
    """Single creative item for table."""
    creative_name: str = Field(..., description="Name of the creative")
    type: str = Field(..., description="Creative type (SHARE, VIDEO, etc.)")
    headline: Optional[str] = Field(None, description="Creative headline")
    ctr: float = Field(..., description="Average Click-Through Rate")
    impressions: int = Field(..., description="Total impressions")
    primary_text: Optional[str] = Field(None, description="Primary text/body copy")
    status: str = Field(..., description="Creative status")


class CreativesResponse(BaseModel):
    """Response model for paginated creatives table."""
    data: List[CreativeItem] = Field(..., description="List of creatives")
    total: int = Field(..., description="Total number of creatives")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")

    class Config:
        from_attributes = True
