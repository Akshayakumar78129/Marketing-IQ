"""
Search & Keywords Match Type - Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class MatchTypeItem(BaseModel):
    """Individual match type performance item."""
    match_type: str = Field(..., description="Match type (EXACT, PHRASE, BROAD)")
    keyword_count: int = Field(..., description="Number of keywords with this match type")
    spend: float = Field(..., description="Total spend for this match type")

    class Config:
        from_attributes = True


class MatchTypeResponse(BaseModel):
    """Response model for match type distribution."""
    match_types: List[MatchTypeItem] = Field(..., description="List of match type performance data")
