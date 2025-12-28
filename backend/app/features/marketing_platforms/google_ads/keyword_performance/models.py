"""
Google Ads Keyword Performance - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class KeywordPerformanceItem(BaseModel):
    """Response model for a single keyword's performance metrics."""
    keyword: str = Field(..., description="Keyword text")
    match: str = Field(..., description="Match type (EXACT, PHRASE, BROAD)")
    impressions: int = Field(..., description="Total impressions")
    clicks: int = Field(..., description="Total clicks")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")
    conversions: int = Field(..., description="Total conversions")
    cost: float = Field(..., description="Total cost/spend")

    class Config:
        from_attributes = True


class KeywordPerformanceResponse(BaseModel):
    """Response model for list of keyword performance metrics."""
    items: list[KeywordPerformanceItem] = Field(..., description="List of keyword performance records")
    total: int = Field(..., description="Total number of keywords")

    class Config:
        from_attributes = True
