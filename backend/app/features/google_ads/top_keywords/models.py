"""
Google Ads Top Keywords - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class TopKeywordItem(BaseModel):
    """Response model for a single top keyword's performance metrics."""
    keyword: str = Field(..., description="Keyword text")
    match_type: str = Field(..., description="Match type (EXACT, PHRASE, BROAD)")
    impressions: int = Field(..., description="Total impressions")
    clicks: int = Field(..., description="Total clicks")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    conversions: int = Field(..., description="Total conversions")
    cost: float = Field(..., description="Total cost/spend")

    class Config:
        from_attributes = True


class TopKeywordsResponse(BaseModel):
    """Response model for list of top keywords."""
    items: list[TopKeywordItem] = Field(..., description="List of top keyword records")
    total: int = Field(..., description="Total number of keywords")

    class Config:
        from_attributes = True
