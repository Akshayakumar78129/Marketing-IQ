"""
Search & Keywords - Keywords Performance Pydantic models (DTOs).
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class KeywordPerformanceItem(BaseModel):
    """Individual keyword performance item."""
    keyword: str = Field(..., description="Keyword text")
    match_type: str = Field(..., description="Match type (EXACT, PHRASE, BROAD)")
    impressions: int = Field(..., description="Total impressions")
    clicks: int = Field(..., description="Total clicks")
    ctr: float = Field(..., description="Click-through rate percentage")
    cpc: float = Field(..., description="Cost per click")
    spend: float = Field(..., description="Total spend")
    conversions: float = Field(..., description="Total conversions")
    conv_rate: float = Field(..., description="Conversion rate percentage")

    class Config:
        from_attributes = True


class KeywordsListResponse(BaseModel):
    """Response model for keywords list."""
    keywords: List[KeywordPerformanceItem] = Field(..., description="List of keyword performance data")
    total_count: int = Field(..., description="Total number of keywords returned")
