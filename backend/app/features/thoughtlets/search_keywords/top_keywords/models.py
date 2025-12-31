"""
Search & Keywords Top Keywords - Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class TopKeywordItem(BaseModel):
    """Individual top keyword item."""
    keyword: str = Field(..., description="Keyword text")
    conversions: float = Field(..., description="Total conversions")
    clicks: int = Field(..., description="Total clicks")

    class Config:
        from_attributes = True


class TopKeywordsResponse(BaseModel):
    """Response model for top keywords list."""
    keywords: List[TopKeywordItem] = Field(..., description="List of top keywords")
