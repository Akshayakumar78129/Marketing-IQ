"""
Meta Ads Demographics Age - Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class MetaAdsDemographicsAgeResponse(BaseModel):
    """Response model for a single age bracket's metrics."""
    age_bracket: str = Field(..., description="Age bracket (18-24, 25-34, etc.)")
    impressions: int = Field(..., description="Total number of impressions")
    spend: float = Field(..., description="Total advertising spend")
    clicks: int = Field(..., description="Total number of clicks")
    reach: int = Field(..., description="Total unique users reached")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")

    class Config:
        from_attributes = True


class MetaAdsDemographicsAgeListResponse(BaseModel):
    """Response model for list of age demographics."""
    demographics: List[MetaAdsDemographicsAgeResponse] = Field(..., description="List of age demographics")
    total_count: int = Field(..., description="Total number of age brackets")

    class Config:
        from_attributes = True
