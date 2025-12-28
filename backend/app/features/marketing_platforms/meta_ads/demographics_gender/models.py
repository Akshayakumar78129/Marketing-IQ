"""
Meta Ads Demographics Gender - Pydantic models (DTOs).
"""
from typing import List
from pydantic import BaseModel, Field


class MetaAdsDemographicsGenderResponse(BaseModel):
    """Response model for a single gender's metrics."""
    gender: str = Field(..., description="Gender (male, female, unknown)")
    impressions: int = Field(..., description="Total number of impressions")
    spend: float = Field(..., description="Total advertising spend")
    clicks: int = Field(..., description="Total number of clicks")
    reach: int = Field(..., description="Total unique users reached")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")

    class Config:
        from_attributes = True


class MetaAdsDemographicsGenderListResponse(BaseModel):
    """Response model for list of gender demographics."""
    demographics: List[MetaAdsDemographicsGenderResponse] = Field(..., description="List of gender demographics")
    total_count: int = Field(..., description="Total number of genders")

    class Config:
        from_attributes = True
