"""
Search & Keywords Overview - Pydantic models (DTOs).
"""
from pydantic import BaseModel, Field


class SearchKeywordsOverviewResponse(BaseModel):
    """Response model for search keywords overview metrics."""
    total_keywords: int = Field(..., description="Total number of unique keywords")
    exact_match: int = Field(..., description="Number of exact match keywords")
    phrase_match: int = Field(..., description="Number of phrase match keywords")
    broad_match: int = Field(..., description="Number of broad match keywords")
    avg_ctr: float = Field(..., description="Average click-through rate percentage")
    avg_cpc: float = Field(..., description="Average cost per click")
    conversions: float = Field(..., description="Total conversions")
    total_spend: float = Field(..., description="Total spend amount")

    class Config:
        from_attributes = True
